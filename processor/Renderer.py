import numpy as np
import cv2

class Renderer():
    
    timeStep1 = 2.0
    timeStep2 = 3.0
    timeStep3 = 8.0
    timeStep4 = 3.0 #timeStep4 要和 timeStep2相等，否则在timeStep4起始中间线区域会跳跃

    timeAcc1 = timeStep1
    timeAcc2 = timeAcc1 + timeStep2
    timeAcc3 = timeAcc2 + timeStep3
    timeAcc4 = timeAcc3 + timeStep4

    def __init__(self):
        self.tickCount = 0
        self.deltaTime = 0
        
    def set_tickCount(self, index):
        # 开启了增强模式，tickCount记录当时的tick数，以便于再次记录时判断走过的时间
        if index == 1:
            self.tickCount = cv2.getTickCount()
        # 1 part -未开启增强模式
        elif index == 0:
            self.tickCount = 0

    def do_Rendering(self, image, adjusters):

        height, width, _ = np.shape(image)
        middle = width // 2

        # 1 part -未开启增强模式
        if self.tickCount <= 0:
            target = image
        
        # 2 part
        elif(self.deltaTime >0 and self.deltaTime <= Renderer.timeAcc1):
            imageCenter = Renderer.get_middle(self, image, 0.5)
            
            target = np.hstack((imageCenter, imageCenter))

        # 3 part
        elif(self.deltaTime <= Renderer.timeAcc2):
            sliderPercent = (self.deltaTime - Renderer.timeAcc1) / Renderer.timeStep2 #local percent
            imageCenter_origin = Renderer.get_middle(self, image, 0.5)
            imageCenter_origin_left_rendering = Renderer.get_left(self, imageCenter_origin, sliderPercent)
            imageCenter_origin_right = Renderer.get_right(self, imageCenter_origin, 1.0 - sliderPercent)
            # frame process with time
            for adjuster in adjusters:
                imageCenter_origin_left_rendering = adjuster.do_it(imageCenter_origin_left_rendering)

            target = np.hstack((imageCenter_origin_left_rendering, imageCenter_origin_right, imageCenter_origin))
            
        # 2 part
        elif(self.deltaTime <= Renderer.timeAcc3):
            imageCenter = Renderer.get_middle(self, image, 0.5)
            imageCenter_rendering = imageCenter
            # frame process with time
            for adjuster in adjusters:
                imageCenter_rendering = adjuster.do_it(imageCenter_rendering)

            target = np.hstack((imageCenter_rendering, imageCenter))

        # 2 part
        elif(self.deltaTime <= Renderer.timeAcc4):
            sliderPercent = (self.deltaTime - Renderer.timeAcc3 + Renderer.timeStep2) / (Renderer.timeStep4 + Renderer.timeStep2)
            imageCenter_rendering = Renderer.get_middle(self, image, sliderPercent)
            # frame process with time
            for adjuster in adjusters:
                imageCenter_rendering = adjuster.do_it(imageCenter_rendering)

            iamgeCenter = Renderer.get_middle(self, image, 0.5)
            imageCenter_right = Renderer.get_left(self, image, 1.0 - sliderPercent)
            
            target = np.hstack((imageCenter_rendering, imageCenter_right))

        else:
            image_rendering = image
            for adjuster in adjusters:
                image_rendering = adjuster.do_it(image_rendering)

            target = image_rendering

        self.deltaTime = (cv2.getTickCount() - self.tickCount) / cv2.getTickFrequency()

        return target

    def get_middle(self, image, percent):
        
        height, width, _ = np.shape(image)
        middle = width // 2
        edge = int(percent * middle)

        begin = middle - edge
        end = middle + edge

        return image[:, begin:end]

    def get_left(self, image, percent):
        height, width, _ = np.shape(image)
        end = int(percent * width)
        
        return image[:, :end]

    def get_right(left, image, percent):
        height, width, _ = np.shape(image)
        begin = int((1.0 - percent) * width)
        
        return image[:, begin:]

    def createTrackerBar(self, windowName):
        cv2.createTrackbar("Render", windowName,
                0, 1, self.set_tickCount)
        