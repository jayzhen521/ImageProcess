import numpy as np
import cv2
from rw import rw


class guidefilter(rw):
    def __init__(self):
        self.ksize = 5
        self.eps = 0.01

    def set_ksize(self, ksize):
        print(ksize)
        self.ksize = (ksize // 2) * 2 + 1

    def get_ksize(self):
        return int(self.ksize)

    def set_eps(self, eps):
        self.eps = eps / 100.0

    def get_eps(self):
        return int(self.eps * 100.0)

    def GuideBlur(self, I, p, winSize, eps):
        mean_I = cv2.blur(I, winSize)      # I的均值平滑
        mean_p = cv2.blur(p, winSize)      # p的均值平滑

        mean_II = cv2.blur(I * I, winSize)  # I*I的均值平滑
        mean_Ip = cv2.blur(I * p, winSize)  # I*p的均值平滑

        var_I = mean_II - mean_I * mean_I  # 方差
        cov_Ip = mean_Ip - mean_I * mean_p  # 协方差

        a = cov_Ip / (var_I + eps)         # 相关因子a
        b = mean_p - a * mean_I            # 相关因子b

        mean_a = cv2.blur(a, winSize)      # 对a进行均值平滑
        mean_b = cv2.blur(b, winSize)      # 对b进行均值平滑

        q = mean_a * I + mean_b
        return q

    def do_blur(self, rgb):
        if self.ksize >= 3:
            ksize = (self.ksize // 2) * 2 + 1
            I = rgb / 255.0

            rgb = np.clip(self.GuideBlur(I, I, (ksize, ksize), self.eps)
                          * 255.0, 0, 255.0).astype(np.uint8)
        return rgb

    def createTrackerBar(self, windowName):
        cv2.createTrackbar("guide::ksize", windowName,
                           self.get_ksize(), 25, self.set_ksize)
        cv2.createTrackbar("guide::eps", windowName,
                           self.get_eps(), 100, self.set_eps)

    def do_it(self, bgr):
        return guidefilter.do_blur(self, bgr)

    def __str__(self):
        return "guidefilter"
