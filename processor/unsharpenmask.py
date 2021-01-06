import numpy as np
import cv2


class unsharpenmask:
    def __init__(self):
        self.ksize = 5
        self.sigma = 5
        self.weight = 0.5

    def set_ksize(self, ksize):
        self.ksize = ksize % 2 + 1

    def set_sigma(self, sigma):
        self.sigma = sigma

    def set_weight(self, weight):
        self.weight = weight / 100.0

    def get_ksize(self):
        return self.ksize

    def get_sigma(self):
        return self.sigma

    def get_weight(self):
        return int(self.weight * 100)

    def do_usm(self, rgb):
        blur = cv2.GaussianBlur(
            rgb, (self.ksize, self.ksize), self.sigma, self.sigma)
        return cv2.addWeighted(rgb, 1.0 + self.weight, blur, -self.weight, 0)
