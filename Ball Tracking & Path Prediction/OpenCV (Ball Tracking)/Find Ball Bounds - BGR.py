import cv2
import numpy as np
video = cv2.VideoCapture(R"D:\DRS\White Ball_Slomo loop.mp4")

lower_bound = np.uint8([186,164,123])
upper_bound = np.uint8([255,255,255])
def Update(x):
     Blue_L = cv2.getTrackbarPos("Blue-L","Controls")
     Green_L = cv2.getTrackbarPos("Green-L","Controls")
     Red_L = cv2.getTrackbarPos("Red-L","Controls")
     Blue_H = cv2.getTrackbarPos("Blue-H","Controls")
     Green_H = cv2.getTrackbarPos("Green-H","Controls")
     Red_H = cv2.getTrackbarPos("Red-H","Controls")
     global lower_bound
     lower_bound = np.uint8([Blue_L,Green_L,Red_L])
     global upper_bound
     upper_bound = np.uint8([Blue_H,Green_H,Red_H])

cv2.namedWindow("Controls")
cv2.createTrackbar("Blue-L","Controls",lower_bound[0],255,Update)
cv2.createTrackbar("Green-L","Controls",lower_bound[1],255,Update)
cv2.createTrackbar("Red-L","Controls",lower_bound[2],255,Update)
cv2.createTrackbar("Blue-H","Controls",upper_bound[0],255,Update)
cv2.createTrackbar("Green-H","Controls",upper_bound[1],255,Update)
cv2.createTrackbar("Red-H","Controls",upper_bound[2],255,Update)

while (video.isOpened()):
    ret, frame = video.read()
    colour_switch = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    height = video.get(4) * 0.3
    width = video.get(3) *0.3
    size = (int(width), int(height))
    resized = cv2.resize(colour_switch, size)
    masked = cv2.inRange(resized, lower_bound, upper_bound)
    bitwised = cv2.bitwise_and(resized, resized, mask = masked)    

    
    
    cv2.imshow("bitwise",bitwised)
    cv2.imshow("Video", resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break      

video.release()
cv2.destroyAllWindows()
print("done")
 