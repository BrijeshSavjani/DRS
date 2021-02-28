import cv2
import numpy as np
video = cv2.VideoCapture(R"D:\DRS\test.mp4")

lower_bound = np.uint8([0,0,0])

upper_bound = np.uint8([179,255,255])
def Update(x):
     Hue_L = cv2.getTrackbarPos("Hue-L","Controls")
     Saturation_L = cv2.getTrackbarPos("Saturation-L","Controls")
     Value_L = cv2.getTrackbarPos("Value-L","Controls")
     Hue_H = cv2.getTrackbarPos("Hue-H","Controls")
     Saturation_H = cv2.getTrackbarPos("Saturation-H","Controls")
     Value_H = cv2.getTrackbarPos("Value-H","Controls")
     global lower_bound
     lower_bound = np.uint8([Hue_L,Saturation_L,Value_L])
     global upper_bound
     upper_bound = np.uint8([Hue_H,Saturation_H,Value_H])

cv2.namedWindow("Controls")
cv2.createTrackbar("Hue-L","Controls",lower_bound[0],179,Update)
cv2.createTrackbar("Saturation-L","Controls",lower_bound[1],255,Update)
cv2.createTrackbar("Value-L","Controls",lower_bound[2],255,Update)
cv2.createTrackbar("Hue-H","Controls",upper_bound[0],179,Update)
cv2.createTrackbar("Saturation-H","Controls",upper_bound[1],255,Update)
cv2.createTrackbar("Value-H","Controls",upper_bound[2],255,Update)

while (video.isOpened()):
    ret, frame = video.read()
    height = video.get(4) * 0.3
    width = video.get(3) *0.3
    size = (int(width), int(height))
    resized = cv2.resize(frame, size)
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    masked = cv2.inRange(hsv, lower_bound, upper_bound)
    bitsize = cv2.bitwise_and(resized, resized, mask = masked)    
    cv2.imshow("video", resized)
    cv2.imshow("bitwise",bitsize)
    cv2.imshow("masked", masked)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break      

video.release()
cv2.destroyAllWindows()
print("done")
 
