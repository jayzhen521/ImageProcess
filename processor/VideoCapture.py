import cv2

class VideoCapture:
    def __init__(self, videoPath):
        self.cap = cv2.VideoCapture(videoPath)
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    def get_cap(self):
        return self.cap

    def get_fps(self):
        return self.fps

    def get_size(self):
        return self.size

    def isOpened(self):
        return self.cap.isOpened()

    def read(self):
        ret, frame = self.cap.read()
        return (ret, frame)

    def release(self):
        self.cap.release()