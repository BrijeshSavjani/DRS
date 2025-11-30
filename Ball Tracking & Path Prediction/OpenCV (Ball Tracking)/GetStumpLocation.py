import numpy as np
import cv2 as cv2

class ImageDrawing: #To-Do: Chnage to throwing errors + properly doc (parameter type hints + what function does hint + return type hint)
    def __init__(self,image:cv2.typing.MatLike):
        self.__image = np.copy(image)
        self.__in_selection = False
        self.__selection_start = [None,None]

    def StartSelection(self,x:int,y:int,image:cv2.typing.MatLike):
        self.__in_selection = True
        self.__selection_start = [x,y]
        self.__image = image

    def TraceOver(self,x:int,y:int)->cv2.typing.MatLike: #Returns new image with selection traced over the top.
        if self.__in_selection:     
            tmp_image = np.copy(self.__image)
            cv2.rectangle(tmp_image,self.__selection_start,(x,y),(0,0,255),1)
            return tmp_image
        else: 
            raise Exception("Not currently in selection so can't trace over")

        
    def EndSelection(self,x:int,y:int)->list: #Returns selection 
        if self.__in_selection:
            self.__in_selection = False
            return [self.__selection_start,[x,y]] #Return bounds of selection drawn
        else:
            raise Exception("Not currently in selection so can't end selection")

    def InSelection(self)->bool: return self.__in_selection #Getter for in_selection
    

 
# mouse callback function
def draw_selection(event,x,y,flags,param):#To-Do: Change to switch. Param?
    global draw,img,stumps_loc
    if event == cv2.EVENT_RBUTTONDOWN:
        draw.StartSelection(x,y,img)
    elif event == cv2.EVENT_MOUSEMOVE and draw.InSelection():
        img = draw.TraceOver(x,y)
    elif event == cv2.EVENT_RBUTTONUP and draw.InSelection():
        stumps_loc = draw.EndSelection(x,y)

def ConvertPixelToM(point,m_per_pixel,video):
        return [(point[0] * m_per_pixel),((video.get(cv2.CAP_PROP_FRAME_HEIGHT) - point[1]) * m_per_pixel)]

def GetStumpLocation(path:str)->list:
    global draw,img,stumps_loc
    video = cv2.VideoCapture(path)
    _,img = video.read()
    draw = ImageDrawing(img)
    stumps_loc = None

    cv2.namedWindow('image', cv2.WINDOW_GUI_NORMAL)
    cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback('image',draw_selection)

    while(stumps_loc is  None):
        cv2.imshow('image',img)
        if cv2.waitKey(20) & 0xFF == 27:
            break

    #convert to m here - 
    m_per_pixel = 0.72 / abs(stumps_loc[0][1]-stumps_loc[1][1])     
    ret = (m_per_pixel,[ConvertPixelToM(stumps_loc[0],m_per_pixel,video),ConvertPixelToM(stumps_loc[1],m_per_pixel,video)])
    
    cv2.destroyAllWindows()
    video.release()
    return ret



#Test
#print(GetStumpLocation(np.zeros((512,512,3), np.uint8)))