import numpy as np
import cv2
from rw import rw


class unsharpenmask(rw):
    def __init__(self):
        self.ksize = 5
        self.sigma = 0
        self.weight = 0.0

    def set_ori_ksize(self, ksize):
        self.ksize = ksize

    def set_ori_sigma(self, sigma):
        self.sigma = sigma

    def set_ori_weight(self, weight):
        self.weight = weight

    def set_ksize(self, ksize):
        print(ksize)
        self.ksize = max(3, (ksize // 2) * 2 + 1)
        print(self.ksize)

    def set_sigma(self, sigma):
        self.sigma = max(1, sigma)

    def set_weight(self, weight):
        self.weight = weight / 10.0

    def get_ksize(self):
        return int(self.ksize)

    def get_sigma(self):
        return self.sigma

    def get_weight(self):
        return int(self.weight * 10.0)

    def do_usm(self, rgb):
        blur = cv2.GaussianBlur(
            rgb, (self.get_ksize(), self.get_ksize()), self.sigma, self.sigma)
        return cv2.addWeighted(rgb, 1.0 + self.weight, blur, -self.weight, 0)

    def createTrackerBar(self, windowName):
        cv2.createTrackbar("usm::ksize", windowName,
                           self.get_ksize(), 25, self.set_ksize)
        cv2.createTrackbar("usm::weight", windowName,
                           self.get_weight(), 100, self.set_weight)

    def do_it(self, bgr):
        return unsharpenmask.do_usm(self, bgr)

    def __str__(self):
        return "unsharpenmask"
