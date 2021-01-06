import numpy as np
import cv2


class unsharpenmask:
    def __init__(self):
        self.ksize = 5
        self.sigma = 5
        self.weight = 0.5

    def set(ksize, sigma, weight):
        self.ksize = ksize
        self.sigma = sigma
        self.weight = weight

    def get_ksize(self):
        return self.ksize

    def get_sigma(self):
        return self.sigma

    def get_weight(self):
        return self.weight

    def do_usm(self, rgb):
        blur = cv2.GaussianBlur(
            rgb, (self.ksize, self.ksize), self.sigma, self.sigma)
        return cv2.addWeighted(rgb, 1.0 + self.weight, blur, -self.weight, 0)
