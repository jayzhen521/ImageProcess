import numpy as np
import cv2
import target_functions as tf
    
# create window
cv2.namedWindow('sharpen_image')
cap = cv2.VideoCapture("goodgirl.mp4")

# createButton("stop", stopCallback, NULL, )


# def stopCallback(state){
#     if(cv2.waitKey(1) & 0xFF == ord(' ')):
#             cv2.waitKey(0)
# }

# cv2.createButton("stop", stopCallback)

cv2.createTrackbar("亮度", "sharpen_image", -50, 50, tf.nothing)
cv2.createTrackbar("模糊半径", "sharpen_image", 1, 25, tf.nothing)
cv2.createTrackbar("weight", "sharpen_image", 0, 2, tf.nothing)

while(cap.isOpened()):
    ret, frame = cap.read()

    if ret is False:
        break

    hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # hsv_image = brightness_adjust(hsv_image, 0.1)

    # hsv_image = tf.histogram_equal(hsv_image, 2)

    brightness_delta = cv2.getTrackbarPos("brightness-delta", 'sharpen_image') / 100.0
    
    hsv_image = tf.brightness_adjust(hsv_image, brightness_delta)

    bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    bgr_image = tf.unsharp_mask(bgr_image, )

    # show
    h, w = frame.shape[:2]
    result = np.zeros([h, w*2, 3], dtype=frame.dtype)
    result[0:h,0:w,:] = frame
    result[0:h,w:2*w,:] = bgr_image
    cv2.putText(result, "original image", (10, 30), cv2.FONT_ITALIC, 1.0, (0, 0, 255), 2)
    cv2.putText(result, "sharpen image", (w+10, 30), cv2.FONT_ITALIC, 1.0, (0, 0, 255), 2)

    cv2.imshow("sharpen_image", result)

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