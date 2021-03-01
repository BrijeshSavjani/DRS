import cv2
import numpy as np
video = cv2.VideoCapture(R"D:\DRS\White Ball.mp4")

lower_bound = np.uint8([186,164,123])
upper_bound = np.uint8([255,255,255])
while (video.isOpened()):
    ret, frame = video.read()
    colour_switch = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    height = video.get(4) * 0.3
    width = video.get(3) *0.3
    size = (int(width), int(height))
    resized = cv2.resize(colour_switch, size)
    masked = cv2.inRange(resized, lower_bound, upper_bound)
    bitwised = cv2.bitwise_and(resized, resized, mask = masked)    
    reduced = cv2.fastNlMeansDenoising(masked,7,7)
    
    contours ,heirachy = cv2.findContours(reduced, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(0,len(contours)):
        rect = cv2.minAreaRect(contours[i])
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(bitwised,[box],0,(0,255,0),2)
    cv2.imshow("bitwise",bitwised)
    cv2.imshow("Video", resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break      

video.release()
cv2.destroyAllWindows()
print("done")
 