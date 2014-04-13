import cv2
import numpy as np
from save import save, hog, deskew
from train_erg_knn import our_classifier, density
from save import load_tracks
from scipy.signal import fftconvolve
knn = our_classifier()


cam = cv2.VideoCapture("videos/MVI_0984.MOV")

tracks = load_tracks()
#cv2.phaseCorrelate(src1,src2)
_,frame= cam.read()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
while True:
    last_frame = frame
    _,frame= cam.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print fftconvolve(last_frame, frame)
    