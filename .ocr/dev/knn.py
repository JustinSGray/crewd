import numpy as np 
from scipy.misc import imread
import cv2
import os

zeros, nines = [], []
for f in os.listdir("digits/0"):
    im = imread("digits/0/"+f)
    im = cv2.resize(im, (20,15)).flatten()
    zeros.append(im)

for f in os.listdir("digits/9"):
    im = imread("digits/9/"+f)
    im = cv2.resize(im, (20,15)).flatten()
    nines.append(im)

data = np.array(zeros + nines, dtype=np.float32)

labels = np.array(7*[0.] + 7*[9.], dtype=np.float32)

knn = cv2.KNearest()
knn.train(data, labels)

# test
ret,result,neighbours,dist = knn.find_nearest(data,k=2)

