import cv2
from PIL import Image
from pytesseract import image_to_string as i2s
import numpy as np
cam = cv2.VideoCapture("data.mp4")

for i in xrange(3000):
    cam.grab()

i=0
k=0
while True:
    _,frame= cam.read()
    cv2.imshow("Processed", frame)
    m,n = frame[0].shape

    corner = (305,155)
    width = 70
    height = 40
    bottom_corner = (corner[0]+width, corner[1]+height)

    sub_frame = frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,:]

    procframe = cv2.cvtColor(sub_frame, cv2.COLOR_BGR2GRAY)
    procframe = cv2.equalizeHist(procframe)
    #procframe = sub_frame[:,:,1]
    #procframe = cv2.medianBlur(procframe,3)
    #procframe = cv2.Canny(procframe, 90, 90)

    cv2.rectangle(frame, corner, bottom_corner, (0, 255, 0), 2)

    frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,0] = procframe
    frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,1] = procframe
    frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,2] = procframe
    if i%30 == 0:
        cv2.imwrite("frames1/%s.png" % str(k), procframe)
        k+=1
    i+=1

    cv2.imshow("Processed", frame)

    pressed = cv2.waitKey(10) & 255

    if pressed == 27: #exit program on 'esc'
        cam.release()
        exit()