import sys
import os
sys.path.append(os.path.split(os.path.abspath(__file__))[0] + "/../processor")

import numpy as np
import cv2
import target_functions as tf

import adapthisteq as ahe
import unsharpenmask as usm
import vibrance as vibrance
import framecontrol
import adjustbright
import localhisteq

use_adapthisteq = False

usmRunner = usm.unsharpenmask()
claheRunner = ahe.adapthisteq()
vibranceRunner = vibrance.vibrance()
frameControl = framecontrol.framecontrol()
adjustBright = adjustbright.adjustbright()
localhisteq = localhisteq.localhisteq()

windowName = "setting"
cv2.namedWindow(windowName)

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

cv2.imshow(windowName, np.zeros((10, 512, 3), np.uint8))


cap = cv2.VideoCapture("videos/goodgirl.mp4")
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

    if use_adapthisteq:
        # 自适应直方图处理
        bgr_image = claheRunner.do_vplane_clahe(bgr_image)
    else:
        bgr_image = localhisteq.do_localhisteq(bgr_image)

    # 自然饱和度
    bgr_image = vibranceRunner.do_vibrance(bgr_image)

    # show
    htich = np.hstack((frame, bgr_image))
    cv2.putText(htich, "original image", (10, 30),
                cv2.FONT_ITALIC, 1.0, (0, 0, 255), 2)
    cv2.putText(htich, "enhance image", (frame.shape[1] + 10, 30),
                cv2.FONT_ITALIC, 1.0, (0, 0, 255), 2)

    cv2.imshow("image", htich)

    # if cv2.waitKey(1):
    #     if 0xFF == ord(' '):
    #         cv2.waitKey(0)
    #     elif 0xFF == ord('q'):
    #         break

    if(cv2.waitKey(1) & 0xFF == ord(' ')):
        cv2.waitKey(0)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
