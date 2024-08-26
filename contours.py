import cv2 as cv
import numpy as np

from region import Region

class ContourFinder:
    # threading properties
    haystack = None
    # search params
    colour = None
    search_area = None
    area_threshold = 50

    # constructor
    def __init__(self, debug=False):
        self.debug = debug

    def updateHaystack(self, haystack):
        self.haystack = haystack

    def searchFor(self, colour, search_area=None, area_threshold = 50):
        self.colour = colour
        self.search_area = search_area
        self.area_threshold = area_threshold
        return self.findContours()

    def findContours(self):
        colour = self.colourToRGB(self.colour)
        lower, upper = colour[0], colour[1]

        offset_x, offset_y = 0, 0

        haystack = self.haystack
        if self.search_area is not None:
            haystack, offset_x, offset_y = self.cropHaystack(haystack, self.search_area.getBounds())

        thresh = cv.inRange(haystack, np.array(lower), np.array(upper))
        contours, _ = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE, offset=(offset_x, offset_y))

        retval = []
        for contour in contours:
            if cv.contourArea(contour) > self.area_threshold:
                retval.append(self.contourToRegion(contour))
        retval.sort(key = Region.regionArea, reverse=True)
        return retval

    @staticmethod
    def cropHaystack(haystack, bounds):
        left, top, right, bottom = bounds
        haystack = haystack[top:bottom, left:right, 0:haystack.shape[2]+1]
        return haystack, left, top

    @staticmethod
    def colourToRGB(name):
        name = name.upper()
        if name == 'BLACK':
            return [0, 0, 0], [100, 100, 100]
        elif name == 'RED':
            return [155, 0, 0], [255, 100, 100]
        elif name == 'GREEN':
            return [0, 155, 0], [100, 255, 100]
        elif name == 'BLUE':
            return [0, 0, 155], [100, 100, 255]
        elif name == 'YELLOW':
            return [155, 155, 0], [255, 255, 100]
        elif name == 'MAGENTA':
            return [155, 0, 155], [255, 100, 255]
        elif name == 'CYAN':
            return [0, 155, 155], [100, 255, 255]
        elif name == 'WHITE':
            return [155, 155, 155], [255, 255, 255]
        else:
            raise ValueError('Not a valid colour.')

    @staticmethod
    def colourToBGR(name):
        name = name.upper()
        if name == 'BLACK':
            return [0, 0, 0], [100, 100, 100]
        elif name == 'BLUE':
            return [155, 0, 0], [255, 100, 100]
        elif name == 'GREEN':
            return [0, 155, 0], [100, 255, 100]
        elif name == 'RED':
            return [0, 0, 155], [100, 100, 255]
        elif name == 'CYAN':
            return [155, 155, 0], [255, 255, 100]
        elif name == 'MAGENTA':
            return [155, 0, 155], [255, 100, 255]
        elif name == 'YELLOW':
            return [0, 155, 155], [100, 255, 255]
        elif name == 'WHITE':
            return [155, 155, 155], [255, 255, 255]
        else:
            raise ValueError('Not a valid colour.')

    @staticmethod
    def contourToRegion(contour):
        rect = cv.minAreaRect(contour)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        _, wh, angle = rect
        x, y = box[1]
        w, h = wh
        return Region(x, y, w, h, rotation=angle, contour=contour)