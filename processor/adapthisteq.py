import numpy as np
import cv2


class adapthisteq:
    def __init__(self):
        self.clipLimit = 0.01
        self.tilesRow = 8
        self.tilesColumn = 8
        self.clahe = cv2.createCLAHE(
            clipLimit=self.clipLimit, tileGridSize=(self.tilesRow, self.tilesColumn))

    def get_clipLimit(self):
        return int(self.clipLimit * 10)

    def get_tilesRow(self):
        return self.tilesRow

    def get_tilesColumn(self):
        return self.tilesColumn

    def set_clipLimit(self, clipLimit):
        self.clipLimit = max(0.01, clipLimit / 10.0)

    def set_tilesRow(self, tilesRow):
        self.tilesRow = max(1, tilesRow)

    def set_tilesColumn(self, tilesColumn):
        self.tilesColumn = max(1, tilesColumn)

    def do_vplane_clahe(self, rgb):
        self.clahe.setClipLimit(self.clipLimit)
        self.clahe.setTilesGridSize((self.tilesRow, self.tilesColumn))

        hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
        hsv[:, :, 2] = self.clahe.apply(hsv[:, :, 2])
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
