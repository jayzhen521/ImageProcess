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
import framecontrol
import adjustbright
import localhisteq


class ImageEnhancement(Cmd):
    intro = '''====Image enhancement, designed by "Searching Center, Energysh"====
    Type help or ? to list commands.
    '''

    def __init__(self):
        usmRunner = usm.unsharpenmask()
        claheRunner = ahe.adapthisteq()
        vibranceRunner = vibrance.vibrance()
        frameControl = framecontrol.framecontrol()
        adjustBright = adjustbright.adjustbright()
        localhisteq = localhisteq.localhisteq()

        windowName = "setting"
        cv2.namedWindow(windowName)

        adjustDataPath = "adjustData/" + adjust_name + ".txt"

        readAdjustData = ""
        if os.path.exists(adjustDataPath):
            with open(adjustDataPath, "r") as f:
                readAdjustData = f.read()

        adjustDataDict = None
        if readAdjustData != "":
            adjustDataDict = json.loads(readAdjustData)
            # print(adjustDataDict[adjust_name])

        if adjustDataDict:
            for adjustItem in adjustDataDict[adjust_name]:
                for key in adjustItem:
                    if key == "unsharpenmask":
                        d = adjustItem[key]
                        usmRunner.set_ksize(d["ksize"])
                        usmRunner.set_sigma(d["sigma"])
                        usmRunner.set_weight(d["weight"])

        trackbarSetting()
    

    def do_adjust(self, argv):
        '''input 3 parameter: filepath adjust_name video_status
    filepath,
    adjust name(snow_scene, forest_scene, asian, white, black... ),
    video status:(Pause, Resume)'''

        parameters = argv.split(' ')

        if parameters and parameters[0] != "exit" and len(parameters) == 3:
            

    def do_exit(self, arg):
        'Stop run'
        print('Stop running')
        # self.close()
        return True

    # trackball control
    def trackbarSetting(self):
        cv2.createTrackbar("vibrance", windowName,
                    vibranceRunner.get_factor(), 100, vibranceRunner.set_factor)
        cv2.createTrackbar("usm::ksize", windowName,
                        usmRunner.get_ksize(), 25, usmRunner.set_ksize)
        cv2.createTrackbar("usm::weight", windowName,
                        usmRunner.get_weight(), 100, usmRunner.set_weight)
        if use_adapthisteq:
            cv2.createTrackbar("clahe::cliplimit", windowName,
                            claheRunner.get_clipLimit(), 100, claheRunner.set_clipLimit)
            cv2.createTrackbar("clahe::tilesRow", windowName,
                            claheRunner.get_tilesRow(), 16, claheRunner.set_tilesRow)
            cv2.createTrackbar("clahe::tilesColumn", windowName,
                            claheRunner.get_tilesColumn(), 16, claheRunner.set_tilesColumn)
        else:
            cv2.createTrackbar("localhist::maxCG", windowName,
                            localhisteq.get_maxCG(), 100, localhisteq.set_maxCG)
            cv2.createTrackbar("localhist::dcoff", windowName,
                            localhisteq.get_DCoff(), 100, localhisteq.set_DCoff)
            cv2.createTrackbar("localhist::ksize", windowName,
                            localhisteq.get_ksize(), 16, localhisteq.set_ksize)

        cv2.createTrackbar("bright", windowName,
                        adjustBright.get_delta(), 50, adjustBright.set_delta)

        cv2.createTrackbar("frame::frameControl", windowName,
                        frameControl.get_ifGetNextFrame(), 1, frameControl.set_ifGetNextFrame)

    def captureSetting(self):
        cap = cv2.VideoCapture(sys.argv[1])

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) *
                2, int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    def resultSetting(self):
        videoWriter = cv2.VideoWriter(
            sys.argv[1] + ".mp4", cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)


if __name__ == '__main__':
    ImageEnhancement().cmdloop()