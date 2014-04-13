import cv2
import numpy as np
from save import save, hog, deskew
from train_erg_knn import our_classifier, density
from save import save_track
knn = our_classifier()


cam = cv2.VideoCapture("videos/MVI_0984.MOV")
#cam = cv2.VideoCapture("videos/MVI_0982.MOV")
# for i in xrange(3000):
#     cam.grab()

frame_track = []

#[496, 22] 65 90
corner = [496, 22]
width = 65
height = 90
_,frame_= cam.read()
ii=0
force = False
while True:
    frame = frame_.copy()
    m,n = frame[0].shape


    bottom_corner = (corner[0]+width, corner[1]+height)

    sub_frame = frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,:]

    #procframe = cv2.cvtColor(sub_frame, cv2.COLOR_BGR2GRAY)
    procframe = sub_frame[:,:,1]
    
    #procframe = cv2.equalizeHist(procframe)
    procframe = cv2.medianBlur(procframe, 3)
    procframe = cv2.adaptiveThreshold(procframe, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                           cv2.THRESH_BINARY,101, 0)

    procframe = 255 - procframe

    im2 = density(cv2.resize(procframe, (25 ,25 )))
    val = np.array(im2, dtype=np.float32).reshape((1,50))
    if not force:
        ret,result,neighbours,dist = knn.find_nearest(val, k=1)
        result = int(result[0][0])

    #procframe =deskew(procframe, procframe.shape)

    cv2.rectangle(frame, tuple(corner), bottom_corner, (0, 255, 0), 2)

    frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,0] = procframe
    frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,1] = procframe
    frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,2] = procframe
    # if i%30 == 0:
    #     cv2.imwrite("frames1/%s.png" % str(k), procframe)
    #     k+=1
    # i+=1
    #print dist[0][0]/1e6
    setcnr = tuple([corner[0]+20, corner[1] + 100])
    cv2.putText(frame, str(result), setcnr, cv2.FONT_HERSHEY_PLAIN, 3, (255,120,120),2)
    cv2.imshow("Processed", frame)
    pressed = cv2.waitKey(10) & 255
    if pressed == 27 or ii > 470: #exit program on 'esc'
        cam.release()
        save_track(frame_track)
        exit()
    elif pressed == 0: #up
        corner[1] += -1
        print corner, width, height
    elif pressed == 3: #right
        corner[0] += 1
        print corner, width, height
    elif pressed == 1: #down
        corner[1] += 1
        print corner, width, height
    elif pressed == 2: #left
        corner[0] += -1
        print corner, width, height
    elif pressed == 97: #right
        width += 5
        print corner, width, height
    elif pressed == 115: #down
        width += -5
        print corner, width, height
    elif pressed == 100: #left
        height += 5
        print corner, width, height
    elif pressed == 102: #left
        height += -5
        print corner, width, height
    elif pressed >= 48 and pressed <=57:
        force = True
        result = pressed - 48
    elif pressed == 99: #left
        track = [ii, corner[0], corner[1], width, height]
        frame_track.append(track)
        _,frame_= cam.read()
        force = False
        ii+=1
    elif pressed !=255:
        print pressed