import cv2
import numpy as np 
from scipy.misc import imread
import os
from save import hog
import pylab

def density(im):
    d1 = [row.sum() for row in im]
    d2 = [col.sum() for col in im.T]

    d = np.array(d1 + d2, dtype=np.float32)
    return d


def files(digit):
    d = []
    for f in os.listdir("digits2/%s" % str(digit)):
        if ".png" not in f:
            continue
        im = imread("digits2/%s/" % str(digit) +f)
        im = cv2.resize(im, (25,25))
        x = density(im)
        d.append(x)
    return d

def our_classifier():
    tdata, tlabels = [], []
    for i in xrange(10):
        datal = files(i)
        m = len(datal)
        tdata += datal
        tlabels += m*[i]
    tdata = np.array(tdata, dtype=np.float32)
    tlabels = np.array(tlabels, dtype=np.float32)

    knn = cv2.KNearest()
    knn.train(tdata,tlabels)
    return knn