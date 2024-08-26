from cv2 import pointPolygonTest, contourArea
from math import radians, cos, sin
from utils import getGaussianDeviation, waitAtLeast

import cv2 as cv
import numpy as np

class Region:
    # properties
    left = 0
    top = 0
    right = 0
    bottom = 0
    width = 0
    height = 0
    centerX = 0
    centerY = 0
    rotation = 0
    contour = None

    def __init__(self, left, top, width, height, rotation=0, contour=None):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.right = left + width# - 1
        self.bottom = top + height# - 1
        self.centerX = round(left + width / 2)
        self.centerY = round(top + height / 2)
        self.rotation = rotation
        self.contour = contour

    def __eq__(self, other):
        if self.left != other.left:
            return False
        if self.top != other.top:
            return False
        if self.width != other.width:
            return False
        if self.height != other.height:
            return False
        if self.rotation != other.rotation:
            return False
        return True

    def __ne__(self, other):
        return not self == other

    def getArea(self):
        return self.width * self.height if self.contour is None else contourArea(self.contour)

    def getBounds(self):
        return self.left, self.top, self.right, self.bottom

    def getPointWithin(self):
        xrad = int(round(self.width/2))-2
        yrad = int(round(self.height/2))-2

        valid = False
        # find a point via rejection sampling
        while not valid:
            devx = getGaussianDeviation(xrad)
            devy = getGaussianDeviation(yrad)
            candidate = (self.centerX + devx, self.centerY + devy)
            candidate = Region.rotatePoint(candidate, (self.left, self.top), self.rotation)
            valid = self.isPointWithin(candidate)
        return candidate

    def isPointWithin(self, candidate):
        x, y = candidate
        if self.contour is None:
            if self.left <= x <= self.right and self.top <= y <= self.bottom:
                return True
            else:
                return False
        else:
            rect = cv.minAreaRect(self.contour)
            box = cv.boxPoints(rect)
            box = np.int0(box)
            if pointPolygonTest(self.contour, candidate, False) == 1:
                return True
            else:
                return False

    @staticmethod
    def fromCoords(left, top, right, bottom):
        return Region(left, top, right-left, bottom-top)

    @staticmethod
    def regionArea(region):
        return region.getArea()

    @staticmethod
    def rotatePoint(point, origin, angle, clockwise = True):
        """
        Rotate a point clockwise by a given angle around a given origin.

        The angle should be given in degrees.
        """
        if not clockwise:
            angle *= -1
        angle = radians(angle)
        c = cos(angle)
        s = sin(angle)

        ox, oy = origin
        px, py = point

        tx = (px - ox)
        ty = (py - oy)

        qx = ox + c * tx - s * ty
        qy = oy + s * tx + c * ty
        return int(qx), int(qy)