from rw import rw

from VideoStatus import VideoStatus

class VideoControl(rw):
    def __init__(self):
        self.videoStatus = VideoStatus.Paused.value

    def get_videoStatus(self):
        return self.videoStatus

    def set_videoStatus(self, videoStatus):
        self.videoStatus = videoStatus

    
