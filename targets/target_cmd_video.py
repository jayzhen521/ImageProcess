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
import autocontrasteq
import VideoControl
import VideoCapture
import guidefilter
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
        self.guideFilter = None
        self.autoContrastEQ = None

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
        self.guideFilter = guidefilter.guidefilter()
        self.autoContrastEQ = autocontrasteq.autocontrasteq()

        # 读文件，如果存在的话
        if os.path.exists(self.outputAdjustDataPath):
            with open(self.outputAdjustDataPath, "r") as f:
                self.outputAdjustData = f.read()
                adjustDataDict = json.loads(self.outputAdjustData)
                # print(adjustDataDict)
                for adjustItem in adjustDataDict[self.outputAdjustDataPath]:
                    for key in adjustItem:
                        if key == "unsharpenmask":
                            d = adjustItem[key]
                            self.usmRunner.set_ori_ksize(d["ksize"])
                            self.usmRunner.set_ori_sigma(d["sigma"])
                            self.usmRunner.set_ori_weight(d["weight"])
                            print(d["ksize"])
                            print(d["sigma"])
                            print(d["weight"])
                            # self.usmRunner = usm.unsharpenmask(d)
                            # print(d)
                        elif key == "vibrance":
                            d = adjustItem[key]
                            self.vibranceRunner.set_ori_intensity(
                                d["intensity"])
                            print(d["intensity"])
                            # self.vibranceRunner = vibrance.vibrance(d)
                            # print(d)
                            # print(self.vibranceRunner.get_intensity())
                        elif key == "adjustbright":
                            d = adjustItem[key]
                            self.adjustBright.set_ori_delta(d["delta"])
                            print(d["delta"])
                            # print(d)
                            # self.adjustBright = adjustbright.adjustbright(d)
                            # print(self.addjustBright.get_delta())
                        elif key == "guidefilter":
                            d = adjustItem[key]
                            self.guideFilter.set_ksize(d["ksize"])
                            self.guideFilter.set_eps(d["eps"])
                        elif key == "autocontrasteq":
                            d = adjustItem[key]
                            self.autoContrastEQ.set_ksize(d["ksize"])
                            self.autoContrastEQ.set_maxCG(d["maxCG"])
                            self.autoContrastEQ.set_DCoff(d["DCoff"])

    def adjustWindowSetting(self):
        cv2.namedWindow(self.windowName)
        cv2.resizeWindow(self.windowName, (400, 512))
        cv2.imshow(self.windowName, np.zeros((10, 512, 3), np.uint8))

    def parameterOperation(self, argv):

        parameters = argv.split(' ')

        if parameters and parameters[0] != "exit" and len(parameters) == 3:
            self.filePath = parameters[0]

            self.outputVideoDataPath = self.filePath + ".avi"

            self.videoCapture = VideoCapture.VideoCapture(self.filePath)
            # 调节输出设定
            self.outputAdjustDataPath = "adjustData/" + parameters[1] + ".txt"

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
                           self.videoControl.get_videoStatus(), 2, self.videoControl.set_videoStatus)
        cv2.createTrackbar("guide::ksize", self.windowName,
                           self.guideFilter.get_ksize(), 25, self.guideFilter.set_ksize)
        cv2.createTrackbar("guide::eps", self.windowName,
                           self.guideFilter.get_eps(), 100, self.guideFilter.set_eps)
        cv2.createTrackbar("ace::maxCG", self.windowName,
                           self.autoContrastEQ.get_maxCG(), 100, self.autoContrastEQ.set_maxCG)
        cv2.createTrackbar("ace::dcoff", self.windowName,
                           self.autoContrastEQ.get_DCoff(), 100, self.autoContrastEQ.set_DCoff)
        cv2.createTrackbar("ace::ksize", self.windowName,
                           self.autoContrastEQ.get_ksize(), 16, self.autoContrastEQ.set_ksize)

    def videoOutputSetting(self):
        print(self.outputVideoDataPath)
        print((self.videoCapture.get_size()[
              0], self.videoCapture.get_size()[1]))
        self.videoWriter = cv2.VideoWriter(
            self.outputVideoDataPath, cv2.VideoWriter_fourcc(
                'I', '4', '2', '0'),
            self.videoCapture.get_fps(), (self.videoCapture.get_size()[0] * 2, self.videoCapture.get_size()[1]))

    def loopRun(self):

        ref, frame = self.videoCapture.read()

        while True:
            # 去噪
            bgr_image = self.guideFilter.doBlur(frame)
            # ACE
            bgr_image = self.autoContrastEQ.do_ace(bgr_image)
            # 加亮
            bgr_image = self.adjustBright.do_adjust(bgr_image)
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
        outputAdjustData = "{\"" + self.outputAdjustDataPath + \
            "\": [" + self.usmRunner.getData()
        + "," + self.vibranceRunner.getData() + "," + self.adjustBright.getData() + \
            "," + self.guideFilter.getData()
        + "," + self.autoContrastEQ.getData() + "]}"

        with open(self.outputAdjustDataPath, "w") as f:
            print(outputAdjustData)
            f.write(outputAdjustData)

    def unInit(self):
        self.videoCapture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    ImageEnhancement().cmdloop()
