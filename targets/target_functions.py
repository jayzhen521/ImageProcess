import numpy as np
import cv2


def histogram_equal(image, index):
    a, b, c = cv2.split(image)
    if index == 0:  # h
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
