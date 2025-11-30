import cv2
import numpy as np
video = cv2.VideoCapture(r"D:\Personal\Downloads\DRS\DRS\Orange Side Trim.mp4")
lower_bound = np.uint8([0])
upper_bound = np.uint8([20])
while (video.isOpened()):
    ret, frame = video.read()
    colour_switch = cv2.split(frame)[0]
    height = int(video.get(4) * 0.3)
    width = int(video.get(3) *0.3)
    size = (width, height) 
    blank = np.ones((height,width,3), np.uint8)
    resized = cv2.resize(colour_switch, size)
    canny = cv2.Canny(resized,200,200)
    masked = cv2.inRange(resized, lower_bound, upper_bound)
    bitwised = cv2.bitwise_and(resized, resized, mask = masked)    
    reduced = cv2.fastNlMeansDenoising(masked,50,50)
    contours ,heirachy = cv2.findContours(reduced, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(contours)
    # cv2.drawContours(resized,contours,-1,(0,255,0),3)
    cv2.imshow("Output",reduced)
    cv2.imshow("bitwise",masked)
    cv2.imshow("Video", resized)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break      

video.release()
cv2.destroyAllWindows()
print("done")
 