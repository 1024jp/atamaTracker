import cv2
import numpy as np

a = np.array([0,0], dtype='float32')
def getXY(img):
    #define the event
    def getxy(event, x, y, flags, param):
        global a
        if event == cv2.EVENT_LBUTTONDOWN :
            a = np.vstack([a, np.hstack([x,y])])
#    img = cv2.imread(imgPath)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', getxy)
    cv2.cv.ShowImage('image', img)
#    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    b = a[1:,:]
    return b
