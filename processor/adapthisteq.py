import numpy as np
import cv2


class adapthisteq:
    def __init__(self):
        self.clipLimit = 1.0
        self.tilesRow = 8
        self.tilesColumn = 8
        self.clahe = cv2.createCLAHE(
            clipLimit=self.clipLimit, tileGridSize=(self.tilesRow, self.tilesColumn))

    def get_clipLimit(self):
        return self.clipLimit

    def get_tilesRow(self):
        return self.tilesRow

    def get_tilesColumn(self):
        return self.tilesColumn

    def set(self, clipLimit, tilesRow, tilesColumn):
        self.clipLimit = clipLimit
        self.tilesRow = tilesRow
        self.tilesColumn = tilesColumn
        self.clahe.setClipLimit(self.clipLimit)
        self.clahe.setTilesGridSize((self.tilesRow, self.tilesColumn))

    def do_vplane_clahe(self, rgb):
        hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = self.clahe.apply(hsv[:, :, 2])
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
