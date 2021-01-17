import numpy as np
import cv2
from rw import rw

class BrightnessContrast(rw):
    
    def __init__(self):
        self.brightness = 0
        self.contrast = 0

    def set_brightness(self, brightness):
        self.brightness = brightness
    
    def get_brightness(self):
        return self.brightness

    def set_contrast(self, contrast):
        self.contrast = contrast

    def get_contrast(self):
        return self.contrast

    def do_brightness(self, bgr):
        if self.brightness != 0:
            if self.brightness > 0:
                shadow = self.brightness
                highlight = 255
            else:
                shadow = 0
                highlight = 255 + self.brightness
            alpha_b = (highlight - shadow)/255
            gamma_b = shadow
            
            # buf是否可以直接从bgr上修改，而非复制
            buf = cv2.addWeighted(bgr, alpha_b, bgr, 0, gamma_b)
        else:
            # 可以直接返回吧，不用copy
            buf = bgr.copy()
        
        return buf

    def do_contrast(self, bgr):
        if self.contrast != 0:
            f = 131*(self.contrast + 127)/(127*(131-self.contrast))
            alpha_c = f
            gamma_c = 127*(1-f)
        
            buf = cv2.addWeighted(bgr, alpha_c, bgr, 0, gamma_c)
        else:
            buf = bgr.copy()

        return buf

    def createTrackerBar(self, windowName):
        # cv2.createTrackbar("Bright", windowName,
        #         self.get_brightness(), 255, self.set_brightness)
        cv2.createTrackbar("Contrast", windowName,
                self.get_contrast(), 127, self.set_contrast)

    def do_it(self, bgr):
        return BrightnessContrast.do_contrast(self, bgr)

    def __str__(self):
        return "BrightnessContrast"