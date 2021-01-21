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
            width = np.shape(image)[1]
            width_image_left = width // 2
            width_image_right = width - width_image_left
            image_left = Renderer.get_middle(self, image, width_image_left)
            image_right = Renderer.get_middle(self, image, width_image_right)
            
            target = np.hstack((image_left, image_right))
            # print(np.shape(target)[1])

        # 3 part
        elif(self.deltaTime <= Renderer.timeAcc2):
            sliderPercent = (self.deltaTime - Renderer.timeAcc1) / Renderer.timeStep2 #local percent
            
            width = np.shape(image)[1]
            width_image_left = width // 2
            width_image_right = width - width_image_left
            image_left = Renderer.get_middle(self, image, width_image_left)
            image_right = Renderer.get_middle(self, image, width_image_right)

            width_image_left_left = int(width_image_left * sliderPercent)
            width_image_left_right = width_image_left - width_image_left_left

            image_left_left = Renderer.get_left(self, image_left, width_image_left_left)
            image_left_right = Renderer.get_right(self, image_left, width_image_left_right)

            # frame process with time
            for adjuster in adjusters:
                image_left_left = adjuster.do_it(image_left_left)

            # print(width_image_left_left + width_image_left_right)
            # print(width_image_right)

            target = np.hstack((np.hstack((image_left_left, image_left_right)), image_right))
            
        # 2 part
        elif(self.deltaTime <= Renderer.timeAcc3):

            width = np.shape(image)[1]
            width_image_left = width // 2
            width_image_right = width - width_image_left
            image_left = Renderer.get_middle(self, image, width_image_left)
            image_right = Renderer.get_middle(self, image, width_image_right)

            # frame process with time
            for adjuster in adjusters:
                image_left = adjuster.do_it(image_left)

            target = np.hstack((image_left, image_right))

        # 2 part
        elif(self.deltaTime <= Renderer.timeAcc4):
            sliderPercent = (self.deltaTime - Renderer.timeAcc3 + Renderer.timeStep2) / (Renderer.timeStep4 + Renderer.timeStep2)

            width = np.shape(image)[1]
            width_image_left_source = width // 2
            width_image_right_source = width - width_image_left_source
            # 获取视频中间部分，作为右部图片的原料
            image_right_source = Renderer.get_middle(self, image, width_image_right_source)

            width_image_left = int(width * sliderPercent)
            width_image_right = width - width_image_left

            image_left = Renderer.get_middle(self, image, width_image_left)
            # print(np.shape(image))
            image_right = Renderer.get_left(self, image_right_source, width_image_right)
            # print(np.shape(image_right_source))
            # frame process with time
            for adjuster in adjusters:
                image_left = adjuster.do_it(image_left)
            
            target = np.hstack((image_left, image_right))

        else:
            image_rendering = image
            for adjuster in adjusters:
                image_rendering = adjuster.do_it(image_rendering)

            target = image_rendering

        self.deltaTime = (cv2.getTickCount() - self.tickCount) / cv2.getTickFrequency()

        return target

    def get_middle(self, image, widthNeeded):

        width = np.shape(image)[1]
        middle = width // 2
        
        widthNeeded_left = widthNeeded // 2
        widthNeeded_right = widthNeeded - widthNeeded_left
        begin = middle - widthNeeded_left
        end = middle + widthNeeded_right

        return image[:, begin:end]

    def get_left(self, image, widthNeeded):
        return image[:, :widthNeeded]

    def get_right(left, image, widthNeeded):
        width = np.shape(image)[1]

        widthNeeded_left = width - widthNeeded
        
        return image[:, widthNeeded_left:]

    def createTrackerBar(self, windowName):
        cv2.createTrackbar("Render", windowName,
                0, 1, self.set_tickCount)
        