import cv2 as cv
import numpy as np

from region import Region

class TemplateMatcher:
    # threading properties
    haystack = None
    # properties
    method = cv.TM_SQDIFF_NORMED #TM_CCORR_NORMED
    # search params
    needle = None
    search_area = None
    use_last_location = True

    # constructor
    def __init__(self, debug=False):
        self.debug = debug

    def updateHaystack(self, haystack):
        self.haystack = haystack

    def searchFor(self, needle, search_area=None, use_last_location=True, error_threshold=0.02):
        self.needle = needle
        self.search_area = search_area
        self.use_last_location = use_last_location
        self.error_threshold = error_threshold
        return self.findMatches()

    def findMatches(self):
        if self.debug:
            print(f"Searching for {self.needle.name}")
        haystack = self.haystack
        offset_x, offset_y = 0, 0
        if self.search_area is not None:
            haystack, dx, dy = self.cropHaystack(haystack, self.search_area.getBounds())
            offset_x += dx
            offset_y += dy
        if self.needle.last_location is not None and self.use_last_location:
            l, t, r, b = self.needle.last_location.getBounds()
            l -= offset_x
            r -= offset_x
            t -= offset_y
            b -= offset_y
            haystack, dx, dy = self.cropHaystack(haystack, (l, t, r, b))
            offset_x += dx
            offset_y += dy

        locations = []
        if self.needle.transparent:
            result = cv.matchTemplate(haystack, self.needle.img, self.method, mask=self.needle.mask)
            result[result == float("inf")] = 0.5 # hack to remove problem values
        else:
            result = cv.matchTemplate(haystack, self.needle.img, self.method)

        # Get the all the positions from the match result that exceed our threshold
        locations = np.where(result <= self.error_threshold)
        locations = list(zip(*locations[::-1]))

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle.width, self.needle.height]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)
        # Apply group rectangles.
        # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
        # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
        # in the result. I've set eps to 0.5, which is:
        # "Relative difference between sides of the rectangles to merge them into a group."
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        # Loop over all the locations and add Regions to return list
        retval = []
        for (x, y, w, h) in rectangles:
            x += offset_x
            y += offset_y
            retval.append(Region(x, y, w, h))
            # set the last location the needle was found in
            self.needle.last_location = retval[-1]
        if self.debug:
            print(f"Found {len(retval)} instances of {self.needle.name}")
        return retval

    @staticmethod
    def cropHaystack(haystack, bounds):
        left, top, right, bottom = bounds
        haystack = haystack[top:bottom, left:right, 0:haystack.shape[2]+1]
        return haystack, left, top