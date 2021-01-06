import numpy as np
import cv2


class vibrance:
    def __init__(self):
        self.intensity = 0.0

    def set_factor(self, factor):
        self.intensity = (factor - 50) / 25.0

    def get_factor(self):
        return int(self.intensity * 25 + 50.0)

    def do_vibrance(self, bgr):
        r = bgr[:, :, 2].astype(np.float64) / 255.0
        g = bgr[:, :, 1].astype(np.float64) / 255.0
        b = bgr[:, :, 0].astype(np.float64) / 255.0

        minColor = np.minimum(np.minimum(r, g), b)
        maxColor = np.maximum(np.maximum(r, g), b)
        color_saturation = maxColor - minColor
        luma = r * 0.072186 + g * 0.715158 + b * 0.212656
        sign_intensity = -1.0 if (self.intensity > 0.0) else 1.0

        cr = 1.0 + self.intensity * (1.0 - sign_intensity * color_saturation)
        cg = 1.0 + self.intensity * (1.0 - sign_intensity * color_saturation)
        cb = 1.0 + self.intensity * (1.0 - sign_intensity * color_saturation)

        fr = np.clip((luma + (r - luma) * cr) *
                     255.0, 0, 255.0).astype(np.uint8)
        fg = np.clip((luma + (g - luma) * cg) *
                     255.0, 0, 255.0).astype(np.uint8)
        fb = np.clip((luma + (b - luma) * cb) *
                     255.0, 0, 255.0).astype(np.uint8)

        saturation = np.stack((fb, fg, fr), -1)
        return saturation
