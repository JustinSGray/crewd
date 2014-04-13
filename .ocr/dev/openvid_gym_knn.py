import cv2
import numpy as np
from save import save, hog, deskew

img = 255 - cv2.imread('digits/digits.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Now we split the image to 5000 cells, each 20x20 size
cells = [np.hsplit(row,100) for row in np.vsplit(gray,50)]

# Make it into a Numpy array. It size will be (50,100,20,20)
x = np.array(cells)

# Now we prepare train_data and test_data.
train = x[:,:50].reshape(-1,400).astype(np.float32) # Size = (2500,400)
test = x[:,50:100].reshape(-1,400).astype(np.float32) # Size = (2500,400)

# Create labels for train and test data
k = np.arange(10)
train_labels = np.repeat(k,250)[:,np.newaxis]
test_labels = train_labels.copy()

# Initiate kNN, train the data, then test it with test data for k=1
knn = cv2.KNearest()
knn.train(train,train_labels)




cam = cv2.VideoCapture("videos/MVI_0984.MOV")
#cam = cv2.VideoCapture("videos/MVI_0982.MOV")
# for i in xrange(3000):
#     cam.grab()

corner = [320,130]
width = 85
height = 135
_,frame_= cam.read()
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

    val = cv2.resize(procframe, (20,20)).reshape(1,400).astype(np.float32)
    ret,result,neighbours,dist = knn.find_nearest(val, k=1)

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
    cv2.putText(frame, str(int(result[0][0])), tuple(corner), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0),2)
    cv2.imshow("Processed", frame)
    pressed = cv2.waitKey(10) & 255
    if pressed == 27: #exit program on 'esc'
        cam.release()
        exit()
    elif pressed == 0: #up
        corner[1] += -5
        print corner, width, height
    elif pressed == 3: #right
        corner[0] += 5
        print corner, width, height
    elif pressed == 1: #down
        corner[1] += 5
        print corner, width, height
    elif pressed == 2: #left
        corner[0] += -5
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
    elif pressed == 99: #left
        _,frame_= cam.read()
    elif pressed >= 48 and pressed <=57:
        save(procframe, pressed - 48)
    elif pressed !=255:
        print pressed