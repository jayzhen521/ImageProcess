import numpy as np
import cv2
from rw import rw
# 很容易出现失真，色块
class HSVAdjuster(rw):

    def __init__(self):
        self.h = 100
        self.s = 100
        self.v = 100

    def set_h(self, h):
        self.h = h

    def get_h(self):
        return self.h

    def set_s(self, s):
        self.s = s

    def get_s(self):
        return self.s

    def set_v(self, v):
        self.v = v

    def get_v(self):
        return self.v

    def do_s(self, bgr):
        image_hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

        h, s, v = cv2.split(image_hsv)
        
        image_hsv = cv2.merge((np.uint8(h), np.uint8(s / 100 * self.s), np.uint8(v)))

        # print(np.uint8(s / 100 * self.s))

        image_bgr = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

        return image_bgr

    def do_it(self, bgr):
        return HSVAdjuster.do_s(self, bgr)

    def createTrackerBar(self, windowName):
        cv2.createTrackbar("Sat", windowName,
                self.get_s(), 200, self.set_s)

    def __str__(self):
        return "HSVAdjuster"
