import numpy as np
import cv2
from rw import rw


class autocontrasteq(rw):
    def __init__(self):
        self.ksize = 7
        self.maxCG = 3
        self.DCoff = 0.5

    def get_maxCG(self):
        return int(10 * self.maxCG)

    def set_maxCG(self, maxcg):
        self.maxCG = maxcg / 10.0

    def get_DCoff(self):
        return int(100 * self.DCoff)

    def set_DCoff(self, DCoff):
        self.DCoff = DCoff / 100.0

    def set_ksize(self, ksize):
        self.ksize = ksize

    def get_ksize(self):
        return self.ksize

    def do_ace(self, rgb):
        ksize = (self.ksize // 2) * 2 + 1
        if self.ksize < 3:
            return rgb

        I = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY).astype(np.int64)
        II = I * I

        mean_lI = cv2.blur(I, (ksize, ksize))  # I的均值平滑
        mean_lII = cv2.blur(II, (ksize, ksize))  # I*I的均值平滑
        var_lI = mean_lII - mean_lI * mean_lI  # 方差

        mean_gI = np.mean(I)
        mean_gII = np.mean(II)
        var_gI = mean_gII - mean_gI * mean_gI

        diff = I - mean_lI
        cg = mean_gI * self.DCoff / \
            np.maximum(np.sqrt(np.maximum(var_lI, 0)), 0.01)
        cg = np.clip(cg, 1.0, self.maxCG)
        newI = mean_lI + diff * cg

        coff = newI / np.maximum(0.01, I)

        return np.clip(rgb * np.stack((coff, coff, coff), -1), 0, 255).astype(np.uint8)
