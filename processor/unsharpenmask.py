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
        self.weight = weight / 25.0

    def get_ksize(self):
        return int(self.ksize)

    def get_sigma(self):
        return self.sigma

    def get_weight(self):
        return int(self.weight * 25.0)

    def do_usm(self, rgb):
        blur = cv2.GaussianBlur(
            rgb, (self.get_ksize(), self.get_ksize()), self.sigma, self.sigma)
        return cv2.addWeighted(rgb, 1.0 + self.weight, blur, -self.weight, 0)

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

    def do_guide_usm(self, rgb):
        I = rgb / 255.0

        blur = np.clip(self.GuideBlur(I, I, (self.get_ksize(), self.get_ksize()), 0.01)
                       * 255.0, 0, 255.0).astype(np.uint8)

        return cv2.addWeighted(rgb, 1.0 + self.weight, blur, -self.weight, 0)
