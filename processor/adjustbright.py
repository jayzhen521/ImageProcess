import numpy as np
import cv2
from rw import rw


class adjustbright(rw):
    def __init__(self):
        self.delta = 0.0
    
    def set_ori_delta(self, delta):
        self.delta = delta

    def get_delta(self):
        return int(self.delta * 100)

    def set_delta(self, delta):
        self.delta = delta / 100.0

    def do_adjust(self, bgr):
        return np.clip(bgr * (1.0 + self.delta), 0, 255).astype(np.uint8)

    def createTrackerBar(self, windowName):
        cv2.createTrackbar("SimpleBright", windowName,
            self.get_delta(), 50, self.set_delta)

    def do_it(self, bgr):
        return adjustbright.do_adjust(self, bgr)

    def __str__(self):
        return "adjustbright"
