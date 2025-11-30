from re import L
import cv2
import numpy as np
video = cv2.VideoCapture(R"D:\DRS\Front-Facing Orange Ball.mp4")

stump_lower_bound = np.uint8([0,60,75]) #BGR
stump_upper_bound = np.uint8([10,100,125])
while (video.isOpened()):
    ret, stump_frame = video.read()
    colour_switch = cv2.cvtColor(stump_frame,cv2.COLOR_RGB2BGR)
    # size = (int(video.get(3) *0.3), int(videqo.get(4) * 0.3))
    # resized = cv2.resize(colour_switch, size)
    masked = cv2.inRange(colour_switch, stump_lower_bound, stump_upper_bound)
    bitwised = cv2.bitwise_and(colour_switch, colour_switch, mask = masked)    
    reduced = cv2.fastNlMeansDenoising(masked,7,7)
    contours ,heirachy = cv2.findContours(reduced, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
         coordinates = str(contours[0]).strip("[").strip("]").split(" ")
         if coordinates != "":
             print(contours[0][0])
    cv2.drawContours(colour_switch,contours,-1,(0,255,0),3)

    cv2.imshow("bitwise",bitwised)
    cv2.imshow("Video", colour_switch)
    cv2.imshow("Mask",masked)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break      

video.release()
cv2.destroyAllWindows()
print("done")
 
