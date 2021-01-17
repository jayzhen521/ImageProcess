from cmd import Cmd
import os
import sys
sys.path.append(os.path.split(os.path.abspath(__file__))[0] + "/../processor")
import json
from collections import namedtuple

import numpy as np
import cv2
import target_functions as tf

from VideoControl import VideoControl
from VideoCapture import VideoCapture
from VideoStatus import VideoStatus
from AdjusterFactory import AdjusterFactory

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

        self.adjusters = []

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

        print("-------" + self.outputAdjustDataPath)

        # 读文件，如果存在的话
        if os.path.exists(self.outputAdjustDataPath):
            with open(self.outputAdjustDataPath, "r") as f:
                self.outputAdjustData = f.read()
                adjustDataDict = json.loads(self.outputAdjustData)
                # print(adjustDataDict)
                # outer loop run only once...
                for adjustItem in adjustDataDict[self.outputAdjustDataPath]:
                    for key in adjustItem:
                        d = adjustItem[key]
                        
                        self.adjusters.append(AdjusterFactory.createAdjuster(key, d))

        else:
            for adjusterName in AdjusterFactory.defaultAdjustersNames:
                self.adjusters.append(AdjusterFactory.createAdjuster(adjusterName))

    def adjustWindowSetting(self):
        cv2.namedWindow(self.windowName)
        cv2.resizeWindow(self.windowName, (400, 512))
        cv2.imshow(self.windowName, np.zeros((10, 512, 3), np.uint8))

    def parameterOperation(self, argv):

        parameters = argv.split(' ')

        if parameters and parameters[0] != "exit" and len(parameters) == 3:
            self.filePath = parameters[0]

            self.outputVideoDataPath = self.filePath + ".mp4"

            self.videoCapture = VideoCapture(self.filePath)
            # 调节输出设定
            self.outputAdjustDataPath = "adjustData/" + parameters[1] + ".txt"

            self.videoControl = VideoControl()

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
        for adjuster in self.adjusters:
            # print(type(adjuster))
            adjuster.createTrackerBar(self.windowName)

        self.videoControl.createTrackerBar(self.windowName)

    def videoOutputSetting(self):
        # print(self.outputVideoDataPath)
        # print((self.videoCapture.get_size()[
        #       0], self.videoCapture.get_size()[1]))
        self.videoWriter = cv2.VideoWriter(
            self.outputVideoDataPath, cv2.VideoWriter_fourcc(*'MJPG'),
            self.videoCapture.get_fps(), (self.videoCapture.get_size()[0] * 2, self.videoCapture.get_size()[1]))

    def loopRun(self):

        ref, frame = self.videoCapture.read()

        while True:
            bgr_image = frame

            for adjuster in self.adjusters:
                bgr_image = adjuster.do_it(bgr_image)

            # show
            htich = np.hstack((frame, bgr_image))
            cv2.putText(htich, "original image", (10, 30),
                        cv2.FONT_ITALIC, 1.0, (0, 0, 255), 2)
            cv2.putText(htich, "enhance image", (frame.shape[1] + 10, 30),
                        cv2.FONT_ITALIC, 1.0, (0, 0, 255), 2)

            self.videoWriter.write(htich)

            cv2.imshow("image", bgr_image)

            if(cv2.waitKey(1) & 0xFF == ord(' ')):
                cv2.waitKey(0)

            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

            if self.videoCapture.isOpened() and self.videoControl.get_videoStatus() == VideoStatus.Playing.value:
                ref, frame = self.videoCapture.read()
                if not ref:
                    self.videoControl.set_videoStatus(VideoStatus.Quit.value)
                    break
            if self.videoControl.get_videoStatus() == VideoStatus.Quit.value:
                break
            else:
                continue

    def videoOutput(self):
        adjusterDataDict = []

        for adjusterObj in self.adjusters:        
            adjusterDataDict.append(adjusterObj.getData())

        with open(self.outputAdjustDataPath, "w") as f:
            f.write(json.dumps({self.outputAdjustDataPath: adjusterDataDict}))

    def unInit(self):
        self.videoWriter.release()
        self.videoCapture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    ImageEnhancement().cmdloop()
