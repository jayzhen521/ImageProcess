from rw import rw
import cv2

from VideoStatus import VideoStatus

class VideoControl(rw):
    def __init__(self):
        self.videoStatus = VideoStatus.Paused.value

    def get_videoStatus(self):
        return self.videoStatus

    def set_videoStatus(self, videoStatus):
        self.videoStatus = videoStatus

    def createTrackerBar(self, windowName):
        cv2.createTrackbar("frame::frameControl", windowName,
            self.get_videoStatus(), 2, self.set_videoStatus)
    
