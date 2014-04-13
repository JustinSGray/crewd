import cv2
from PIL import Image
from pytesseract import image_to_string as i2s
import numpy as np
cam = cv2.VideoCapture(0)

while True:
    _,frame = cam.read()
    #cv2.imshow("Original", frame)
    m,n = frame[0].shape

    corner = (250,100)
    width = 200
    height = 300
    bottom_corner = (corner[0]+width, corner[1]+height)

    sub_frame = frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,:]


    #procframe = cv2.cvtColor(sub_frame, cv2.COLOR_BGR2GRAY)
    procframe = sub_frame[:,:,1]

    procframe = cv2.medianBlur(procframe,3)
    procframe = 255 - procframe
    #procframe = cv2.equalizeHist(procframe)
    #ret3,procframe = cv2.threshold(procframe,0,255,cv2.THRESH_OTSU)
    #procframe = cv2.Canny(procframe, 90, 90)

    cv2.rectangle(frame, corner, bottom_corner, (0, 255, 0), 2)

    
    # procframe = cv2.Canny(procframe, 10, 50)

    # blur = cv2.GaussianBlur(procframe,(3,3),0)
    # ret3,procframe = cv2.threshold(blur,0,255,cv2.THRESH_OTSU)

    pil_frame = Image.fromarray(procframe)
    
    text = i2s(pil_frame).strip()

    if len(text):
        print() 
        print(text)

    frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,0] = procframe
    frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,1] = procframe
    frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,2] = procframe


    cv2.imshow("Processed", frame)

    pressed = cv2.waitKey(10) & 255

    if pressed == 27: #exit program on 'esc'
        cam.release()
        exit()