from cmd import Cmd
import os
import sys
sys.path.append(os.path.split(os.path.abspath(__file__))[0] + "/../processor")
import json
from collections import namedtuple

import numpy as np
import cv2
import target_functions as tf

import adapthisteq as ahe
import unsharpenmask as usm
import vibrance as vibrance
import adjustbright
import localhisteq
import VideoControl
import VideoCapture
from VideoStatus import VideoStatus

# output variables
# outputAdjustData, outputAdjustDataPath
# outputVideoData, outputVideoDataPath

class ImageEnhancement(Cmd):
    intro = '''====Image enhancement, designed by "Searching Center, Energysh"====
    Type help or ? to list commands.
    '''

    def __init__(self):
        super(ImageEnhancement, self).__init__()

        self.filePath = None

        self.outputAdjustData = None
        self.outputAdjustDataPath = None
        self.outputVideoData = None
        self.outputVideoDataPath = None

        self.videoWriter = None

        self.videoControl = None

        self.usmRunner = None
        self.vibranceRunner = None
        self.adjustBright = None

        self.windowName = "AdjustWindow"

        self.videoCapture = None

    def do_adjust(self, argv):
        '''input 3 parameter: filepath adjust_name video_status
            filepath,
            adjust name(snow_scene, forest_scene, asian, white, black... ),
            video status:(Playing, Pause)
        '''

        self.parameterOperation(argv)

        self.adjusterInit()
        
        self.adjustWindowSetting()

        self.trackbarSetting()

        self.videoOutputSetting()

        self.loopRun()
    
        self.videoOutput()

        self.unInit()

    # 锐化、饱和度、亮度调节对象
    def adjusterInit(self):
        
        self.usmRunner = usm.unsharpenmask()
        self.vibranceRunner = vibrance.vibrance()
        self.adjustBright = adjustbright.adjustbright()


    def adjustWindowSetting(self):
        cv2.namedWindow(self.windowName)
        cv2.resizeWindow(self.windowName, (400, 512))
        cv2.imshow(self.windowName, np.zeros((10, 512, 3), np.uint8))
        
            
    def parameterOperation(self, argv):

        parameters = argv.split(' ')

        if parameters and parameters[0] != "exit" and len(parameters) == 3:
            filePath = parameters[0]

            self.outputVideoDataPath = filePath + ".mp4"

            self.videoCapture = VideoCapture.VideoCapture(filePath)
            # 调节输出设定
            outputAdjustDataPath = "adjustData/" + parameters[1] + ".txt"

            self.videoControl = VideoControl.VideoControl()

            if parameters[2] == "Play":
                self.videoControl.set_videoStatus(VideoStatus['Playing'].value)
            elif parameters[2] == "Pause":
                self.videoControl.set_videoStatus(VideoStatus['Paused'].value)
            

    def do_exit(self, arg):
        'Stop run'
        print('Stop running')
        # self.close()
        return True

    # trackball control
    def trackbarSetting(self):
        # trackbar设定
        cv2.createTrackbar("vibrance", self.windowName,
                   self.vibranceRunner.get_factor(), 100, self.vibranceRunner.set_factor)
        cv2.createTrackbar("usm::ksize", self.windowName,
                        self.usmRunner.get_ksize(), 25, self.usmRunner.set_ksize)
        cv2.createTrackbar("usm::weight", self.windowName,
                        self.usmRunner.get_weight(), 100, self.usmRunner.set_weight)
        cv2.createTrackbar("bright", self.windowName,
                        self.adjustBright.get_delta(), 50, self.adjustBright.set_delta)
        cv2.createTrackbar("frame::frameControl", self.windowName,
                        self.videoControl.get_videoStatus(), 1, self.videoControl.set_videoStatus)

    def videoOutputSetting(self):
        if self.videoCapture:
            print(self.videoCapture.get_size())
        self.videoWriter = cv2.VideoWriter(
            self.outputVideoDataPath, cv2.VideoWriter_fourcc('I', '4', '2', '0'),
            self.videoCapture.get_fps(), (self.videoCapture.get_size()[0] * 2, self.videoCapture.get_size()[1]))

    def loopRun(self):

        ref, frame = self.videoCapture.read()

        while True:
            # 加亮
            bgr_image = self.adjustBright.do_adjust(frame)
            # 锐化
            bgr_image = self.usmRunner.do_usm(bgr_image)
            # 自然饱和度
            bgr_image = self.vibranceRunner.do_vibrance(bgr_image)

            # show
            htich = np.hstack((frame, bgr_image))
            cv2.putText(htich, "original image", (10, 30),
                        cv2.FONT_ITALIC, 1.0, (0, 0, 255), 2)
            cv2.putText(htich, "enhance image", (frame.shape[1] + 10, 30),
                        cv2.FONT_ITALIC, 1.0, (0, 0, 255), 2)

            cv2.imshow("image", htich)

            self.videoWriter.write(htich)

            if(cv2.waitKey(1) & 0xFF == ord(' ')):
                cv2.waitKey(0)

            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

            if self.videoCapture.isOpened() and self.videoControl.get_videoStatus() == VideoStatus.Playing.value:
                ref, frame = self.videoCapture.read()
                if not ref:
                    break
            else:
                continue


    def videoOutput(self):
        outputAdjustData = "{\"" + self.outputAdjustDataPath + "\": [" + self.usmRunner.getData() + "," + self.claheRunner.getData() + "," + self.vibranceRunner.getData() + "," + self.adjustBright.getData() + "]}"

        with open(self.outputAdjustDataPath, "w") as f:
            print(outputAdjustData)
            f.write(outputAdjustData)

    def unInit(self):
        cap.release()
        cv2.destroyAllWindows()



if __name__ == '__main__':
    ImageEnhancement().cmdloop()