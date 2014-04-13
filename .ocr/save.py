import cv2
import time
import numpy as np
import pickle
import os
affine_flags = cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR


def load_tracks():
    d = []
    for f in os.listdir("tracks"):
        if ".dat" not in f:
            continue
        track = load_track("tracks/"+f)
        d.append(track)
    return d

def save_track(tracks):
    pickle.dump( tracks, open( "track.dat", "wb" ) )

def load_track(fn):
    return pickle.load( open( fn, "rb" ) )

def save(im, digit):
    n = str(int(time.time()*10) % 1000000)
    cv2.imwrite("digits2/%s/%s.png" % (str(digit), n), im)

def deskew(img, SZ=(20,20)):
    m = cv2.moments(img)
    if abs(m['mu02']) < 1e-2:
        return img.copy()
    skew = m['mu11']/m['mu02']
    M = np.float32([[1, skew, -0.5*SZ[0]*skew], [0, 1, 0]])

    img = cv2.warpAffine(img,M,SZ,flags=affine_flags)
    return img

def hog(img):
    bin_n = 16
    gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
    gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
    mag, ang = cv2.cartToPolar(gx, gy)

    # quantizing binvalues in (0...16)
    bins = np.int32(bin_n*ang/(2*np.pi))

    # Divide to 4 sub-squares
    bin_cells = bins[:10,:10], bins[10:,:10], bins[:10,10:], bins[10:,10:]
    mag_cells = mag[:10,:10], mag[10:,:10], mag[:10,10:], mag[10:,10:]
    hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
    hist = np.hstack(hists)
    return hist