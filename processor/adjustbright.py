import numpy as np
import cv2
from rw import rw


class adjustbright(rw):
    def __init__(self):
        self.delta = 0.0

    def get_delta(self):
        return int(self.delta * 100)

    def set_delta(self, delta):
        self.delta = delta / 100.0

    def do_adjust(self, bgr):
        return np.clip(bgr * (1.0 + self.delta), 0, 255).astype(np.uint8)
