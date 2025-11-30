import numpy as np
import cv2 as cv

class ImageDrawing: #To-Do: Chnage to throwing errors + properly doc (parameter type hints + what function does hint + return type hint)
    def __init__(self,image):
        self.__image = np.copy(image)
        self.__in_selection = False
        self.__selection_start = [None,None]

    def StartSelection(self,x,y,image):
        self.__in_selection = True
        self.__selection_start = [x,y]
        self.__image = image

    def TraceOver(self,x,y): #Returns new image with selection traced over the top. Retruns None if not in selection!
        if self.__in_selection:
            tmp_image = np.copy(self.__image)
            cv.rectangle(tmp_image,self.__selection_start,(x,y),(0,0,255),1)
            return tmp_image
        
    def EndSelection(self,x,y): #Returns selection if tehre is one else returns None!
        if self.__in_selection:
            self.__in_selection = False
            return [self.__selection_start,[x,y]] #Return bounds of selection drawn

    def InSelection(self): return self.__in_selection #Getter for in_selection
    

 
# mouse callback function
def draw_selection(event,x,y,flags,param):#To-Do: CHange to switch. Param?
    global draw,img
    if event == cv.EVENT_RBUTTONDOWN:
        draw.StartSelection(x,y,img)
    elif event == cv.EVENT_MOUSEMOVE and draw.InSelection():
        img = draw.TraceOver(x,y)
    elif event == cv.EVENT_RBUTTONUP and draw.InSelection():
        print(draw.EndSelection(x,y))

# Create a black image, a window and bind the function to window
img = np.zeros((512,512,3), np.uint8)
draw = ImageDrawing(np.copy(img))
cv.namedWindow('image', cv.WINDOW_GUI_NORMAL)
cv.resizeWindow('image',img.shape[0]+100,img.shape[1]+100)
cv.setMouseCallback('image',draw_selection)

while(1):
    cv.imshow('image',img)
    if cv.waitKey(20) & 0xFF == 27:
        break
cv.destroyAllWindows()