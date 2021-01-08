import numpy as np
import cv2


class localhisteq:
    def __init__(self):
        self.k0 = 0.0
        self.k1 = 0.25
        self.s0 = 0
        self.s1 = 0.1
        self.C = 2
        self.ksize = 7
        self.print = False

    def get_k0(self):
        return int(100 * self.k0)

    def get_k1(self):
        return int(100 * self.k1)

    def get_s0(self):
        return int(100 * self.s0)

    def get_s1(self):
        return int(100 * self.s1)

    def set_k0(self, k0):
        self.k0 = k0 / 100.0

    def set_k1(self, k1):
        self.k1 = k1 / 100.0

    def set_s0(self, s0):
        self.s0 = s0 / 100.0

    def set_s1(self, s1):
        self.s1 = s1 / 100.0

    def set_C(self, c):
        self.C = c / 10.0

    def get_C(self):
        return int(10 * self.C)

    def set_ksize(self, ksize):
        self.ksize = max(3, ksize)

    def get_ksize(self):
        return self.ksize

    def do_localhisteq(self, rgb):
        I = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY).astype(np.int64)
        II = I * I

        mean_lI = cv2.blur(I, (self.ksize, self.ksize))  # I的均值平滑
        mean_lII = cv2.blur(II, (self.ksize, self.ksize))  # I*I的均值平滑
        var_lI = mean_lII - mean_lI * mean_lI  # 方差

        mean_gI = np.mean(I)
        mean_gII = np.mean(II)
        var_gI = mean_gII - mean_gI * mean_gI

        comk0 = mean_lI >= self.k0 * mean_gI
        comk1 = mean_lI <= self.k1 * mean_gI
        coms0 = var_lI >= self.s0 * var_gI
        coms1 = var_lI <= self.s1 * var_gI

        coff = 1 + comk0 * comk1 * coms0 * coms1 * (self.C - 1.0)
        mean_coff = cv2.GaussianBlur(coff, (7, 7), 0)

        return np.clip(rgb * np.stack((mean_coff, mean_coff, mean_coff), -1), 0, 255).astype(np.uint8)
