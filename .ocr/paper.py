import cv2
import numpy as np
from save import save, hog, deskew
from train_erg_knn import our_classifier, density
knn = our_classifier()


cam = cv2.VideoCapture(0)


corner = (300,200)
width = 30
height = 60
bottom_corner = (corner[0]+width, corner[1]+height)

while True:
    _,frame= cam.read()
    m,n = frame[0].shape

    sub_frame = frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,:]

    procframe = sub_frame[:,:,1]
    
    procframe = cv2.medianBlur(procframe, 3)
    procframe = cv2.adaptiveThreshold(procframe, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                           cv2.THRESH_BINARY,101, 0)

    procframe = 255 - procframe

    im2 = density(cv2.resize(procframe, (25 ,25 )))
    val = np.array(im2, dtype=np.float32).reshape((1,50))
    ret,result,neighbours,dist =  knn.find_nearest(val, k=1)
    result = int(result[0][0])

    frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,0] = procframe
    frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,1] = procframe
    frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,2] = procframe
    cv2.rectangle(frame, corner, bottom_corner, (0, 255, 0), 1)

    setcnr = tuple([corner[0], corner[1]])
    cv2.putText(frame, str(result), setcnr, cv2.FONT_HERSHEY_PLAIN, 6, (10,255,10),5)

    cv2.imshow("Processed", frame)
    pressed = cv2.waitKey(10) & 255
    if pressed == 27: #exit program on 'esc'
        cam.release()
        exit()