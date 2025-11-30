import cv2
import numpy as np
from Kalman import Kalman
class BallTracker:
    
    def __init__(self,video_path,ball_upper_bound,ball_lower_bound,m_per_pixel,horrizontal=True,):
        #OpenCV Objects
        self.__video = cv2.VideoCapture(video_path)
        self.__background_sub = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50, detectShadows=True)

        #Parameters for tracking
        self.__biateral_d = 15
        self.__bilatreal_sigma_space = 50
        self.__bilateral_sigma_colour = 25
        self.__morphology_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)) #for opening & closing mask
        self.__kalman_variance = 0.1 #Variance for covariance matrix Q in kalman filter    
        self.__ball_lower_bound = ball_lower_bound
        self.__ball_upper_bound = ball_upper_bound                                   

        #Data Variables     
        self.__m_per_pixel = m_per_pixel 
        self.__dt = self.__video.get(cv2.CAP_PROP_FPS)**-1 #seconds per frame
        self.__var_ball_r = (5 * self.__m_per_pixel) ** 2 #5 pixel jitter for centroid
        self.__horrizontal = horrizontal
        self.__video_height = self.__video.get(cv2.CAP_PROP_FRAME_HEIGHT)

        #Learn background - if transiitioning to live then swap for learning to a fixed amount of time (e.g 5 seconds before you start tracking)
        while(self.__video.isOpened()): 
            ret,frame = self.__video.read()
            if ret: self.__background_sub.apply(frame) 
            else: break

        self.__video.set(cv2.CAP_PROP_POS_FRAMES, 0)#reset to start
    

    def __GetContourCentroid(self,contour):
            moments = cv2.moments(contour)
            return (int(moments["m10"]/moments["m00"]),int(moments["m01"]/moments["m00"])) #as (x,y)

    def __ConvertToM(self,point):
        return np.array([[(point[0] * self.__m_per_pixel)],[((self.__video_height - point[1]) * self.__m_per_pixel)]])

    def __ConvertToPixels(self,point):
        return (int(point[0]/self.__m_per_pixel), int((self.__video_height - (point[1]/self.__m_per_pixel))))

    def __GetDistance(self,prediction,contour):
        return np.sqrt((contour[0]-prediction[0])**2 + (contour[1]-prediction[1])**2)

    def __GetNearestContour(self,prediction,contours):
        nearest_contour = (contours[0],self.__GetDistance(prediction,self.__ConvertToM(self.__GetContourCentroid(contours[0]))))
        for contour in contours[1:]: 
            distance = self.__GetDistance(prediction,self.__ConvertToM(self.__GetContourCentroid(contour)))
            if (distance < nearest_contour[1]): nearest_contour = (contour,distance)
        return nearest_contour[0]

    def NextVideo(self,path): #To track next ball (FROM SAME CAMERA AT SAME TIME)
         self.__video = cv2.VideoCapture(path)
         #Don't need to do anything else like background training or anything else as this was allready done for previous video

    def TrackBall(self):
        #Tracking variables
        ball_hit_pad_frame = -1 #Frame user says ball hit pad
        frames_since_last_reset = -1 #-1 if not been reset
        ball_spotted_frame = -1 #Ball not spotted yet
        frame_num = 0 #what frame we're currently on. Inits to 0 because first frame should be 1
        max_contour_size = 500 if self.__horrizontal else 900 #500 pixels^2 - increases if front-on video

        points = [] #Points ball is at

        '''
        Kalman Filter Init Variables

        Explanation:
            Derived using SUVAT equations (s = ut + 1/2at^2; v = u + at)
            Linear filter so assuming constant acceleration (not entirely accurate but have a large Q to overcome)
                -> For better accuracy we could use a UKF ot particle filter 
        
        What they are:
            Model state: [x y vx vy ax ay]

            A = | 1 0 t 0 0.5t^2    0   |
                | 0 1 0 t    0   0.5t^2 |
                | 0 0 1 0    t      0   |
                | 0 0 0 1    0      t   |
                | 0 0 0 0    1      0   |
                | 0 0 0 0    0      1   |


            B = | 0 |
                | 0 |
                | 0 |
                | 0 |
                | 0 |
                | 0 |

            H = | 1 0 0 0 0 0 |
                | 0 1 0 0 0 0 |

    '''
        dt = self.__dt #Done here so matrices still look neat
        var_ball_r = self.__var_ball_r#Done here so matrices still look neat

        Kf = None #Assigned when first spotted
        A_matrix = np.array([
                            [1,0,dt,0,(0.5*(dt**2)),0],
                            [0,1,0,dt,0,(0.5*(dt**2))],
                            [0,0,1,0,dt,0],
                            [0,0,0,1,0,dt],
                            [0,0,0,0,1,0],
                            [0,0,0,0,0,1]
                        ])
        H_matrix = np.array([
                            [1,0,0,0,0,0],
                            [0,1,0,0,0,0]
                        ]) 
        Q_matrix = np.array([
                            [0.01,0,0,0,0,0], #x -  confident
                            [0,0.01,0,0,0,0], #y -  confident                   
                            [0,0,0.1,0,0,0], #v_x - Fairly confident
                            [0,0,0,0.1,0,0], #v_y - Fairly confidemt
                            [0,0,0,0,10,0], #a_x - Not very confident
                            [0,0,0,0,0,5]  #a_y - Somewhat confident
                        ],float)
        init_covariance = np.array ([
                                    [var_ball_r,0,0,0,0,0], #x
                                    [0,var_ball_r,0,0,0,0], #y                
                                    [0,0,10000,0,0,0], #v_x 
                                    [0,0,0,10000,0,0], #v_y 
                                    [0,0,0,0,10000,0], #a_x
                                    [0,0,0,0,0,1000]  #a_y
                                ])      
        R_matrix = np.array([
                            [var_ball_r,var_ball_r],
                            [var_ball_r,var_ball_r] #3 pixel jitter for centroid
                        ])

        #Main loop
        while (self.__video.isOpened()):
            ret, frame = self.__video.read()
            if not ret: break

            if frames_since_last_reset != -1: frames_since_last_reset += 1

            frame_num += 1

            ycrcb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2YCR_CB)
            #Noise removal on Cr plane only as this is most pivotal for orange ball - Switch to Cb if blue-y ball or to whole image if another colour
            ycrcb_frame[:,:,1] = cv2.bilateralFilter(ycrcb_frame[:,:,1],self.__biateral_d,self.__bilateral_sigma_colour,self.__bilatreal_sigma_space)

            #Ball Masks
            colour_mask = cv2.inRange(ycrcb_frame,self.__ball_lower_bound,self.__ball_upper_bound)
            _,motion_mask = cv2.threshold(self.__background_sub.apply(frame,0),127,255,cv2.THRESH_BINARY) #Already learned background
            mask =  colour_mask & motion_mask
            cv2.morphologyEx(mask,cv2.MORPH_OPEN,self.__morphology_kernel,mask)  #Opening(Removing specks/noise)
            cv2.morphologyEx(mask,cv2.MORPH_CLOSE,self.__morphology_kernel,mask) #Closing(Filling in holes of detected ball)

            #If front-facing camera then scale size down as ball will first be quite large as its close to frame before gradually reducing in size    
            if (not self.__horrizontal) & (max_contour_size > 500) & (ball_spotted_frame!=-1):
                max_contour_size *= 0.95
             
            #Get contours
            contours,_   = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #As we're calculating centroid anyway, inner points don't matter and hence heireachy also doesn't matter
            contour_list = list(filter(lambda ball_candidate: 10 < cv2.contourArea(ball_candidate) < max_contour_size,contours))#filter out contours that are too big e.g) players ot too small i.e noise

            #Track ball
            if(ball_spotted_frame!=-1) & (len(contour_list) > 0 & (frame_num <= ball_hit_pad_frame)):#Ball has been seen before and can currently be seen 
                prediction = Kf.Predict()
                current_pos = self.__GetContourCentroid(self.__GetNearestContour(prediction,contour_list))
                res = Kf.RunStepWithoutPredict(self.__ConvertToM(current_pos))

                #Draw prediction,observed value and Kalman value on frame(mostly for debugging)
                cv2.circle(frame,self.__ConvertToPixels((res[0,0],res[1,0])),5,(255,255,255),-1)
              
                points.append((res[0,0],res[1,0]))
                #Hypothesis test to 99% certainty in Chi-Squared distribution that value is wrong/unexpected - Mosy likely fue to bounce. 3 frame cap to prevent constant new filters in case that happens
                if(Kf.GetNIS() >= 9.21):
                    if (frames_since_last_reset == -1) or (frames_since_last_reset >=3):
                        current_pos_m = self.__ConvertToM(current_pos)
                        initial_state = np.array([[current_pos_m[0,0]],[current_pos_m[1,0]],[0],[0],[0],[-9.81]])
                        Kf = Kalman(A_matrix=A_matrix,x0=initial_state,Q_k=Q_matrix,H_k=H_matrix,R_k=R_matrix,p0=init_covariance,variance=self.__kalman_variance)
                        frames_since_last_reset = 0
            elif (ball_spotted_frame!=-1):#Occlusion (Ball has been seen before but can't currently be seen most likely behind soemthing) or gone past when ball has hit pad
                res = Kf.RunFullStep()
                current_pos = self.__ConvertToPixels((res[0,0],res[1,0]))
                cv2.circle(frame,current_pos,5,(255,255,255),-1)
                points.append((res[0,0],res[1,0]))
            #If this is first time seeing ball start kalman
            elif (ball_spotted_frame == -1) & (len(contour_list) > 0): #Note: Logically this should be first in if-elif statements but more effieicient if at bottom
                ball_spotted_frame = frame_num
                current_pos_m = self.__ConvertToM(self.__GetContourCentroid(contour_list[0]))
                initial_state = np.array([[current_pos_m[0,0]],[current_pos_m[1,0]],[0],[0],[0],[-9.81]])
                Kf = Kalman(A_matrix=A_matrix,x0=initial_state,Q_k=Q_matrix,H_k=H_matrix,R_k=R_matrix,p0=init_covariance,variance=self.__kalman_variance)
                cv2.circle(frame, self.__ConvertToPixels(current_pos_m), 5, (255, 255, 255), -1) #Draw dot ontop of ball
                points.append((current_pos_m[0,0],current_pos_m[1,0]))
            cv2.imshow("f",frame)
            wait_key = cv2.waitKey(1)
            if wait_key & 0xFF == ord('h'):
                ball_hit_pad_frame = frame_num
            if wait_key & 0xFF == ord('q'):
                break
            elif wait_key & 0xFF == ord('r'):
                self.__video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ball_spotted_frame = -1
        
        cv2.destroyAllWindows()
        self.__video.release()
        ball_hit_pad_frame_normalised = (ball_hit_pad_frame - ball_spotted_frame) if ball_hit_pad_frame != -1 else -1
        return (dt,points,ball_hit_pad_frame_normalised)


#Parameter definitions - For test
# path = r"D:\Personal\Downloads\DRS\DRS\Orange Front Trim.mp4"
# ball_lower_bound = np.uint8([0,160,0])
# ball_upper_bound = np.uint8([255,255,255])

# #Test
# bt = BallTracker(path,ball_upper_bound,ball_lower_bound,(0.72/156),False)
# print(bt.TrackBall())