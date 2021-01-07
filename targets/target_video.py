import sys
import os
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

# command parameter 
if len(sys.argv) <= 1:
    print("error, please enter video path.")
    sys.exit()

if_getNextFrame = 0
if len(sys.argv) >= 3:
    if sys.argv[2] == "True":
        if_getNextFrame = 1

if_imShowRun = True
if len(sys.argv) >= 4:
    if sys.argv[3] == "False":
        if_imShowRun = False

adjust_name = "default"
if len(sys.argv) >= 5:
    adjust_name = sys.argv[4]


usmRunner = usm.unsharpenmask()
claheRunner = ahe.adapthisteq()
vibranceRunner = vibrance.vibrance()
frameControl = framecontrol.framecontrol()
adjustBright = adjustbright.adjustbright()

adjustDataPath = "adjustData/" + adjust_name + ".txt"

readAdjustData = ""
if os.path.exists(adjustDataPath):
    with open(adjustDataPath, "r") as f:
        readAdjustData = f.read()

if readAdjustData != "":
    adjustDataDict = json.loads(readAdjustData)
    # print(adjustDataDict[adjust_name])

for adjustItem in adjustDataDict[adjust_name]:
    for key in adjustItem:
        if key == "unsharpenmask":
            d = adjustItem[key]
            usmRunner.set_ksize(d["ksize"])
            usmRunner.set_sigma(d["sigma"])
            usmRunner.set_weight(d["weight"])

windowName = "setting"
cv2.namedWindow(windowName)



frameControl.set_ifGetNextFrame(if_getNextFrame)

cv2.createTrackbar("vibrance", windowName,
                   vibranceRunner.get_factor(), 100, vibranceRunner.set_factor)
cv2.createTrackbar("usm::ksize", windowName,
                   usmRunner.get_ksize(), 25, usmRunner.set_ksize)
cv2.createTrackbar("usm::weight", windowName,
                   usmRunner.get_weight(), 100, usmRunner.set_weight)
cv2.createTrackbar("clahe::cliplimit", windowName,
                   claheRunner.get_clipLimit(), 100, claheRunner.set_clipLimit)
cv2.createTrackbar("clahe::tilesRow", windowName,
                   claheRunner.get_tilesRow(), 16, claheRunner.set_tilesRow)
cv2.createTrackbar("clahe::tilesColumn", windowName,
                   claheRunner.get_tilesColumn(), 16, claheRunner.set_tilesColumn)

cv2.createTrackbar("bright", windowName,
                   adjustBright.get_delta(), 50, adjustBright.set_delta)

cv2.createTrackbar("frame::frameControl", windowName,
                   frameControl.get_ifGetNextFrame(), 1, frameControl.set_ifGetNextFrame)

cv2.resizeWindow(windowName, (400, 512))
cv2.imshow(windowName, np.zeros((10, 512, 3), np.uint8))

cap = cv2.VideoCapture(sys.argv[1])

fps =int(cap.get(cv2.CAP_PROP_FPS))
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * 2, int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
videoWriter = cv2.VideoWriter(sys.argv[1] + ".mp4", cv2.VideoWriter_fourcc('I','4','2','0'), fps, size)

while(cap.isOpened()):

    if frameControl.get_isFirstFrame() or frameControl.get_ifGetNextFrame():
        ret, frame = cap.read()
        frameControl.set_isFirstFrame(False)

        if ret is False:
            break

    # 加亮
    bgr_image = adjustBright.do_adjust(frame)
    # 锐化
    bgr_image = usmRunner.do_usm(bgr_image)
    # # 自适应直方图处理
    # bgr_image = claheRunner.do_vplane_clahe(bgr_image)
    # 自然饱和度
    bgr_image = vibranceRunner.do_vibrance(bgr_image)

    # show
    htich = np.hstack((frame, bgr_image))
    cv2.putText(htich, "original image", (10, 30),
                cv2.FONT_ITALIC, 1.0, (0, 0, 255), 2)
    cv2.putText(htich, "enhance image", (frame.shape[1] + 10, 30),
                cv2.FONT_ITALIC, 1.0, (0, 0, 255), 2)



    if if_imShowRun:
        cv2.imshow("image", htich)

    videoWriter.write(htich)
    

    # if cv2.waitKey(1):
    #     if 0xFF == ord(' '):
    #         cv2.waitKey(0)
    #     elif 0xFF == ord('q'):
    #         break

    if(cv2.waitKey(1) & 0xFF == ord(' ')):
        cv2.waitKey(0)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

adjustData = "{\"" + adjust_name + "\": [" + usmRunner.getData() + "," + claheRunner.getData() + "," + vibranceRunner.getData() + "," + adjustBright.getData() + "]}"

with open("adjustData/" + adjust_name + ".txt", "w") as f:
    f.write(adjustData)

cap.release()
cv2.destroyAllWindows()
