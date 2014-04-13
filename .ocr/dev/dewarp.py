import numpy as np 
import pylab
from scipy.misc import imread
import cv2

img = cv2.imread('digits/display.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

back = np.zeros((600,600))

back[200:486, 200:465] = img




rows,cols = img.shape

pts1 = np.float32([[200,200], [200, 465], [486, 200], [486,465]])
pts2 = np.float32([[210,210],[210,440],[504,200],[500,500]])

M = cv2.getPerspectiveTransform(pts1,pts2)

dst = cv2.warpPerspective(img,M,(600,600))

pylab.subplot(121)
pylab.imshow(back)
pylab.subplot(122)
pylab.imshow(dst)
pylab.show()
quit()