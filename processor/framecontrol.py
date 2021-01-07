from rw import rw

class framecontrol(rw):
    def __init__(self):
        self.isFirstFrame = True
        self.ifGetNextFrame = 0

    def get_isFirstFrame(self):
        return self.isFirstFrame

    def set_isFirstFrame(self, isFirst):
        self.isFirstFrame = isFirst

    def get_ifGetNextFrame(self):
        return self.ifGetNextFrame

    def set_ifGetNextFrame(self, ifGetNext):
        self.ifGetNextFrame = ifGetNext

    
