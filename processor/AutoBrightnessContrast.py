import numpy as np
import cv2
from rw import rw

class AutoBrightnessContrast(rw):
    
    def __init__(self):
        self.clipHistPercent = 1

    def get_clipHistPercent(self):
        return self.clipHistPercent

    def set_clipHistPercent(self, clipHistPercent):
        self.clipHistPercent = clipHistPercent
    
    def createTrackerBar(self, windowName):
        # cv2.createTrackbar("Bright", windowName,
        #         self.get_brightness(), 255, self.set_brightness)
        cv2.createTrackbar("AutoContrast", windowName,
                self.get_clipHistPercent(), 127, self.set_clipHistPercent)

    def do_it(self, bgr):
        clip_hist_percent = self.clipHistPercent
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

        # Calculate grayscale histogram
        hist = cv2.calcHist([gray],[0],None,[256],[0,256])
        hist_size = len(hist)

        # Calculate cumulative distribution from the histogram
        accumulator = []
        accumulator.append(float(hist[0]))
        for index in range(1, hist_size):
            accumulator.append(accumulator[index -1] + float(hist[index]))

        # Locate points to clip
        maximum = accumulator[-1]
        clip_hist_percent *= (maximum/100.0)
        clip_hist_percent /= 2.0

        # Locate left cut
        minimum_gray = 0
        while accumulator[minimum_gray] < clip_hist_percent:
            minimum_gray += 1

        # Locate right cut
        maximum_gray = hist_size -1
        while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
            maximum_gray -= 1

        # Calculate alpha and beta values
        alpha = 255 / (maximum_gray - minimum_gray)
        beta = -minimum_gray * alpha

        '''
        # Calculate new histogram with desired range and show histogram 
        new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
        plt.plot(hist)
        plt.plot(new_hist)
        plt.xlim([0,256])
        plt.show()
        '''
        # print("alpha = {}, beta = {}".format(alpha, beta))

        image = cv2.convertScaleAbs(bgr, alpha=alpha, beta=beta)
        return image

    def __str__(self):
        return "AutoBrightnessContrast"