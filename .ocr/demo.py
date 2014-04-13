import cv2
import numpy as np
from save import save, hog, deskew
from train_erg_knn import our_classifier, density
from save import load_tracks
knn = our_classifier()
import pylab

cam = cv2.VideoCapture("videos/MVI_0984.MOV")

#fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
# fourcc =  cv2.cv.CV_FOURCC('i','Y','U', 'V')
# out = cv2.VideoWriter('output.mpg',fourcc, 30.0, (1280,720))

tracks = load_tracks()
#cv2.phaseCorrelate(src1,src2)

ii=0
times = []
while True:
    _,frame= cam.read()
    display_frame = np.copy(frame)
    m,n = frame[0].shape
    pframes = []
    t_frame = []
    for track in tracks:
        idx, cornerx, cornery, width, height = track[ii]
        corner = (cornerx, cornery)
        bottom_corner = (corner[0]+width, corner[1]+height)

        sub_frame = frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,:]

        procframe = sub_frame[:,:,1]
        
        procframe = cv2.medianBlur(procframe, 3)
        procframe = cv2.adaptiveThreshold(procframe, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                               cv2.THRESH_BINARY,101, 0)

        procframe = 255 - procframe

        im2 = density(cv2.resize(procframe, (25 ,25 )))
        val = np.array(im2, dtype=np.float32).reshape((1,50))
        ret,result,neighbours,dist = knn.find_nearest(val, k=1)
        result = int(result[0][0])
        t_frame.append(result)

        cv2.rectangle(display_frame, tuple(corner), bottom_corner, (0, 255, 0), 2)
        setcnr = tuple([corner[0]+20, corner[1] + 100])
        cv2.putText(display_frame, str(result), setcnr, cv2.FONT_HERSHEY_PLAIN, 6, (255,255,255),5)
        #display_frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,0] = procframe
        #display_frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,1] = procframe
        #display_frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,2] = procframe
    print t_frame
    t= t_frame[0]*60 + int(str(t_frame[1]) + str(t_frame[2]))
    times.append(t)
    ii+=1
    cv2.imshow("Processed", display_frame)

    pressed = cv2.waitKey(10) & 255
    if pressed == 27 or ii > 470: #exit program on 'esc'
        cam.release()
        pylab.plot(times)
        pylab.show()
