import cv2
import numpy as np
video = cv2.VideoCapture(R"D:\DRS\CropWB.mp4")

lower_bound = np.uint8([186,164,123])
upper_bound = np.uint8([255,255,255])
while (video.isOpened()):
    ret, frame = video.read()
    colour_switch = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    height = int(video.get(4) * 0.3)
    width = int(video.get(3) *0.3)
    size = (width, height)
    blank = np.ones((height,width,3), np.uint8)
    resized = cv2.resize(colour_switch, size)
    masked = cv2.inRange(resized, lower_bound, upper_bound)
    bitwised = cv2.bitwise_and(resized, resized, mask = masked)    
    reduced = cv2.fastNlMeansDenoising(masked,7,7)
    try:
        contours ,heirachy = cv2.findContours(reduced, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        maximumArea = cv2.contourArea(contours[0])
        for i in range(0,len(contours)):
            area = cv2.contourArea(contours[i])
            if  int(area) > 1 and int(area) < 12:
                cv2.drawContours(blank,contours,i,(0,255,0),-3)
                if max([maximumArea,area]) == area:
                    maximumArea = area
    except:
        print("error")
    cv2.imshow("Output",blank)
    cv2.imshow("bitwise",bitwised)
    cv2.imshow("Video", resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break      

video.release()
cv2.destroyAllWindows()
print("done")
 