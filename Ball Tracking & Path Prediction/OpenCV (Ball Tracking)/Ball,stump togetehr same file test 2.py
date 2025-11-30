import cv2
import numpy as np
video = cv2.VideoCapture(R"D:\Personal\Downloads\DRS\DRS\Orange Front Trim.mp4")
ball_export = open(R"D:\Personal\Downloads\DRS\DRS\ball_location_data.txt", "w")
stump_export = open(R"D:\Personal\Downloads\DRS\DRS\stump_location_data.txt", "w")


ball_lower_bound = np.uint8([0,105,167]) #HSL
ball_upper_bound = np.uint8([8,192,255])
stump_lower_bound = np.uint8([80,113,104]) #HSL
stump_upper_bound = np.uint8([102,209,212])

def ExitTracking():
        video.release()
        cv2.destroyAllWindows()
        ball_export.close()
        stump_export.close()
        print("done")
        
while (video.isOpened()):
    try:
        ret, frame = video.read()
        colour_switch = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        resized = cv2.resize(colour_switch, (int(video.get(3) *0.3), int(video.get(4) * 0.3)))
        ball_masked = cv2.inRange(resized, ball_lower_bound, ball_upper_bound)
        stump_masked = cv2.inRange(resized, stump_lower_bound, stump_upper_bound)   
        ball_reduced = cv2.fastNlMeansDenoising(ball_masked,7,21)
        stump_reduced = cv2.fastNlMeansDenoising(stump_masked,7,21)
        ball_contours ,heirachy = cv2.findContours(ball_reduced, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        stump_contours ,heirachy = cv2.findContours(stump_reduced, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

        ball_export.write(str(ball_contours) + '/n')
        stump_export.write(str(stump_contours) + '/n')

        cv2.drawContours(resized,ball_contours,-1,(0,255,0),3)
        cv2.drawContours(resized,stump_contours,-1,(255,0,0),3)


        cv2.imshow("Stumps",stump_masked)
        cv2.imshow("Video", resized)
        cv2.imshow("Ball",ball_masked)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            ExitTracking()
            break      
    except:
        ExitTracking()

