from re import L
import cv2
import numpy as np
video = cv2.VideoCapture(R"D:\DRS\Orange Ball.mp4")

ball_lower_bound = np.uint8([180,0,40]) #BGR
ball_upper_bound = np.uint8([240,80,120])
while (video.isOpened()):
    ret, ball_frame = video.read()
    colour_switch = cv2.cvtColor(ball_frame,cv2.COLOR_RGB2BGR)
    size = (int(video.get(3) *0.3), int(video.get(4) * 0.3))
    resized = cv2.resize(colour_switch, size)
    masked = cv2.inRange(resized, ball_lower_bound, ball_upper_bound)
    bitwised = cv2.bitwise_and(resized, resized, mask = masked)    
    reduced = cv2.fastNlMeansDenoising(masked,7,7)
    contours ,heirachy = cv2.findContours(reduced, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        coordinates = str(contours[0]).strip("[").strip("]").split(" ")
        if coordinates != "":
            print(contours[0][0])
    cv2.drawContours(resized,contours,-1,(0,255,0),3)

    cv2.imshow("bitwise",bitwised)
    cv2.imshow("Video", resized)
    cv2.imshow("Mask",masked)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break      

video.release()
cv2.destroyAllWindows()
print("done")
 
