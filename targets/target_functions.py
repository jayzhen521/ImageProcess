import numpy as np
import cv2

def brightness_adjust(image, delta):
    image[:,:,2] = np.clip(image[:,:,2] * (1.0 + delta), 0, 255)
    return image

def histogram_equal(image, index):
    a, b, c = cv2.split(image)
    if index == 0: #h
        equ = cv2.equalizeHist(a)
        res = np.hstack((a, equ))
        image = cv2.merge((a, b, equ))
    elif index == 1:
        equ = cv2.equalizeHist(b)
        res = np.hstack((b, equ))
        image = cv2.merge((a, b, equ))
    elif index == 2:
        equ = cv2.equalizeHist(c)
        res = np.hstack((c, equ))
        image = cv2.merge((a, b, equ))

    return image

def bgr2hsv(image):
    cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return image

def unsharp_mask(image, sigmaX, weight):
    blur_img = cv2.GaussianBlur(image, (0, 0), sigmaX)
    image = cv2.addWeighted(image, 1.0 + weight, blur_img, -weight, 0)

    return image

def nothing(x):
    pass