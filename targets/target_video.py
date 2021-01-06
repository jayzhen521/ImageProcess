import sys
import os
sys.path.append(os.path.split(os.path.abspath(__file__))[0] + "/../processor")

import numpy as np
import cv2
import target_functions as tf

import adapthisteq as ahe
import unsharpenmask as usm
import vibrance as vibrance

usmRunner = usm.unsharpenmask()
claheRunner = ahe.adapthisteq()
vibranceRunner = vibrance.vibrance()

windowName = "leftEye"
cv2.namedWindow(windowName)

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

cv2.createTrackbar("addbright(*1%)", windowName, 0, 50, tf.nothing)


cap = cv2.VideoCapture("videos/goodgirl.mp4")
while(cap.isOpened()):
    ret, frame = cap.read()

    if ret is False:
        break

    brightness_delta = cv2.getTrackbarPos(
        "addbright(*1%)", windowName) / 100.0

    # 加亮
    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_image = tf.brightness_adjust(hsv_image, brightness_delta)
    bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    # 锐化
    bgr_image = usmRunner.do_usm(bgr_image)
    # 自适应直方图处理
    bgr_image = claheRunner.do_vplane_clahe(bgr_image)
    # 自然饱和度
    bgr_image = vibranceRunner.do_vibrance(bgr_image)

    # show
    h, w = frame.shape[:2]
    htich = np.hstack((frame, bgr_image))
    cv2.putText(htich, "original image", (10, 30),
                cv2.FONT_ITALIC, 1.0, (0, 0, 255), 2)
    cv2.putText(htich, "sharpen image", (w + 10, 30),
                cv2.FONT_ITALIC, 1.0, (0, 0, 255), 2)

    cv2.imshow(windowName, htich)

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
