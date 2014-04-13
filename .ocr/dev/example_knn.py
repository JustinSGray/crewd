import numpy as np
import cv2

cam = cv2.VideoCapture(0)

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
# ret,result,neighbours,dist = knn.find_nearest(test)

while True:
    _,frame = cam.read()
    #cv2.imshow("Original", frame)
    m,n = frame[0].shape

    corner = (300,200)
    width = 50
    height = 50
    bottom_corner = (corner[0]+width, corner[1]+height)

    sub_frame = frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,:]

    procframe = cv2.cvtColor(sub_frame, cv2.COLOR_BGR2GRAY)
    #procframe = 255 - procframe
    #procframe = cv2.equalizeHist(procframe)
    frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,0] = procframe
    frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,1] = procframe
    frame[corner[1]:corner[1]+height, corner[0]:corner[0]+width,2] = procframe
    cv2.rectangle(frame, corner, bottom_corner, (0, 255, 0), 1)
    val = cv2.resize(procframe, (20,20)).reshape(1,400).astype(np.float32)

    ret,result,neighbours,dist = knn.find_nearest(val, k=1)
    score = np.linalg.norm(dist) / 1.e6
    #print result, score
    cv2.putText(frame, str(int(result[0][0])), (300,200), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0),2)

    cv2.imshow("Processed", frame)
    pressed = cv2.waitKey(10) & 255
    if pressed == 27: #exit program on 'esc'
        cam.release()
        exit()