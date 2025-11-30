import cv2
import numpy as np

video = cv2.VideoCapture(r"D:\Personal\Downloads\DRS\DRS\Orange Side Trim.mp4")
global paused
paused = False

def Update(x):
     Hue_L = cv2.getTrackbarPos("Hue-L","Controls")
     Saturation_L = cv2.getTrackbarPos("Saturation-L","Controls")
     Value_L = cv2.getTrackbarPos("Value-L","Controls")
     Hue_H = cv2.getTrackbarPos("Hue-H","Controls")
     Saturation_H = cv2.getTrackbarPos("Saturation-H","Controls")
     Value_H = cv2.getTrackbarPos("Value-H","Controls")
     Playback_Speed = cv2.getTrackbarPos("Playback-Speed","Controls")
     global lower_bound
     lower_bound = np.uint8([max(Hue_L,0),max(Saturation_L,0),max(0,Value_L)])
     global upper_bound
     upper_bound = np.uint8([max(Hue_H,0),max(Saturation_H,0),max(Value_H,0)])
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
cv2.createTrackbar("Hue-L","Controls",0,179,Update)
cv2.createTrackbar("Saturation-L","Controls",105,255,Update)
cv2.createTrackbar("Value-L","Controls",167,255,Update)

cv2.createTrackbar("Hue-H","Controls",7,179,Update)
cv2.createTrackbar("Saturation-H","Controls",192,255,Update)
cv2.createTrackbar("Value-H","Controls",255,255,Update)
cv2.createTrackbar("Playback-Speed","Controls",500,1000,Update)
cv2.createTrackbar("Pause","Controls",0,1,handlePause)


height = video.get(4) * 0.3
width = video.get(3) *0.3
size = (int(width), int(height))  #Too big for screen otherwise

while (video.isOpened()):
    if not paused:
        ret, frame = video.read()
    else:
        ret = True
    if  ret:
        resized = cv2.resize(frame,size)
        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
        masked = cv2.inRange(hsv, lower_bound, upper_bound)
        bitwise = cv2.bitwise_and(resized, resized, mask = masked)    
        
        origin_videos = addTitles([resized,hsv,cv2.cvtColor(resized, cv2.COLOR_BGR2LAB)],["Orignal","HSV","lab"])
        cv2.imshow("Controls",origin_videos)
        
        result_videos = addTitles([bitwise,cv2.cvtColor(masked,cv2.COLOR_GRAY2BGR)],["Bitwise","Masked"])
        cv2.imshow("Bitwise & mask",result_videos)

        l, a, b = cv2.split(cv2.cvtColor(resized, cv2.COLOR_BGR2LAB))
        #y = cv2.convertScaleAbs(y,(255/180))
        individual_chanels = addTitles([cv2.cvtColor(l,cv2.COLOR_GRAY2BGR),cv2.cvtColor(a,cv2.COLOR_GRAY2BGR),cv2.cvtColor(b,cv2.COLOR_GRAY2BGR)],["L","A", "B"])
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
 
