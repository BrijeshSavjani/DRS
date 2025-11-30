import cv2
import numpy as np

def GetBallBounds(path):
    video = cv2.VideoCapture(path)
    global paused
    paused = False

    def Update(x):
         Y_L = cv2.getTrackbarPos("Y-L","Controls")
         CR_L = cv2.getTrackbarPos("CR-L","Controls")
         CB_L = cv2.getTrackbarPos("CB-L","Controls")
         Y_H = cv2.getTrackbarPos("Y-H","Controls")
         CR_H = cv2.getTrackbarPos("CR-H","Controls")
         CB_H = cv2.getTrackbarPos("CB-H","Controls")


         Playback_Speed = cv2.getTrackbarPos("Playback-Speed","Controls")
         global lower_bound
         lower_bound = np.uint8([max(Y_L,0),max(CR_L,0),max(CB_L,0)])
         global upper_bound
         upper_bound = np.uint8([max(Y_H,0),max(CR_H,0),max(CB_H,0)])
         global playback_speed
         playback_speed = Playback_Speed

    def addTitles(frames,titles):
        if len(frames) != len(titles):
            print("ERROR: Frames length not equal to titles length")
            return
        width = []
        for frame in frames:
            width.append(frame.shape[1])

        title_bar = np.zeros((30,sum(width),3), dtype=np.uint8)

        current_width = 0
        for i in range(0,len(frames)):
            cv2.putText(
                img = title_bar,
                text = titles[i],
                org= ((10 + current_width),20),
                fontFace= cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=0.5,
                color=(255,255,255),
                thickness=1
            )
            current_width += width[i]

        frame_stack = np.hstack(frames)
        return np.vstack((title_bar,frame_stack))
    def handlePause(x):
        global paused
        paused = bool(x)

    cv2.namedWindow("Controls")
    cv2.createTrackbar("Y-L","Controls",0,255,Update)
    cv2.createTrackbar("CR-L","Controls",172,255,Update)
    cv2.createTrackbar("CB-L","Controls",0,255,Update)

    cv2.createTrackbar("Y-H","Controls",255,255,Update)
    cv2.createTrackbar("CR-H","Controls",255,255,Update)
    cv2.createTrackbar("CB-H","Controls",128,255,Update)


    cv2.createTrackbar("Playback-Speed","Controls",500,1000,Update)
    cv2.createTrackbar("Pause","Controls",0,1,handlePause)


    height = video.get(4) * 0.3
    width = video.get(3) *0.3
    size = (int(width), int(height))  #Too big for screen otherwise

    while (video.isOpened()):
        if not paused:
            ret, frame = video.read()
        else: ret = True #If paused automatically let code run
        if  ret:
            resized = cv2.resize(frame,size)
            lab = cv2.cvtColor(resized, cv2.COLOR_BGR2YCR_CB)
            masked = cv2.inRange(lab, lower_bound, upper_bound)
            bitwise = cv2.bitwise_and(resized, resized, mask = masked)    

            origin_videos = addTitles([resized,lab],["ORIGNAL", "YCrCb"])
            cv2.imshow("Controls",origin_videos)

            result_videos = addTitles([bitwise,cv2.cvtColor(masked,cv2.COLOR_GRAY2BGR)],["Bitwise","Masked"])
            cv2.imshow("Bitwise & mask",result_videos)

            y, cr, cb = cv2.split(lab)
            individual_chanels = addTitles([cv2.cvtColor(y,cv2.COLOR_GRAY2BGR),cv2.cvtColor(cr,cv2.COLOR_GRAY2BGR),cv2.cvtColor(cb,cv2.COLOR_GRAY2BGR)],["Y","Cr", "Cb"])
            cv2.imshow("Individual LAB",individual_chanels)
            #Not hugely helpful

        wait_key = cv2.waitKey(playback_speed)
        if (wait_key & 0xFF == ord('q')) or not ret :
            break      
        elif (wait_key & 0xFF == 32):
            paused = not paused 
            cv2.setTrackbarPos("Pause","Controls",int(paused)) #Update status on GUI
        elif (wait_key & 0xFF == ord('r')):
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            cv2.setTrackbarPos("Pause","Controls",0) #Ensure video plays after pause by unpausing cideo + updating GUI

    video.release()
    cv2.destroyAllWindows()
    print("done")
    return((lower_bound),(upper_bound))
    
 
#Test
#print(GetBallBounds(path=r"D:\Personal\Downloads\DRS\DRS\Orange Side Trim.mp4"))