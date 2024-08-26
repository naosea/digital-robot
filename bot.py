from region import Region
from needle import Needle
from outputs import MouseController
from templates import TemplateMatcher
from contours import ContourFinder
from time import time
from threading import Thread, Lock

from utils import waitAtLeast

class Script():
    debug = False
    screenshot = None
    display = 0
    window_coords = (0, 0, 0, 0)
    locations = []
    search_areas = []
    search_area_names = []
    #inv = Region.fromCoords(969, 381, 1315, 869)
    #chat = Region.fromCoords(1, 633, 777, 842)
    #bank = Region.fromCoords(108, 5, 837, 628)
    #search_areas.append(inv)
    #search_areas.append(chat)
    #search_areas.append(bank)
    #search_area_names.append("inv")
    #search_area_names.append("chat")
    #search_area_names.append("bank")# https://tutswiki.com/read-write-config-files-in-python/

    def __init__(self, debug=False):
        self.debug = debug
        self.lock = Lock()
        self.stopped = False
        self.mc = MouseController(debug=debug)
        self.tm = TemplateMatcher(debug=debug)
        self.cf = ContourFinder(debug=debug)

    # threading methods
    def start(self):
        print("Starting in: 3")
        waitAtLeast(1)
        print("Starting in: 2")
        waitAtLeast(1)
        print("Starting in: 1")
        waitAtLeast(1)
        print("Go!")
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            if self.screenshot is None:
                continue
            self.main()
        print("Script stopped")

    def updateScreenshot(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def main(self):
        # This should be implemented in subclass
        waitAtLeast(0)

    def moveInto(self, region, fast=False):
        if region is None:
            return
        self.mc.move(region, self.display, self.window_coords, fast=fast)

    def clickIn(self, region, right_click=False, shift=False, fast=False):
        self.moveInto(region, fast=fast)
        self.mc.click(right_click=right_click, shift=shift)

    def press(self, key):
        self.mc.press(key)

    def clickAll(self, regions, right_click=False, shift=False, fast=False):
        if shift:
            self.mc.hold("shift")
        for region in regions:
            self.clickIn(region, right_click=right_click, fast=fast)
        if shift:
            self.mc.release("shift")

    def find(self, target, **kwargs):
        if isinstance(target, Needle):
            return self.findNeedle(target, **kwargs)
        else:
            return self.findContour(target, **kwargs)

    def findAll(self, target, **kwargs):
        if isinstance(target, Needle):
            return self.findAllNeedles(target, use_last_location=False, **kwargs)
        else:
            return self.findAllContours(target, **kwargs)

    def findNeedle(self, needle, **kwargs):
        locs = self.findAllNeedles(needle, **kwargs)
        if len(locs) == 0:
            return None
        else:
            return locs[0]

    def findContour(self, color, **kwargs):
        locs = self.findAllContours(color, **kwargs)
        if len(locs) == 0:
            return None
        else:
            return locs[0]

    def findAllNeedles(self, needle, search_area=None, use_last_location=True, max_search_time = float('inf'), error_threshold = 0.02):
        locs = []
        start_time = time()
        while len(locs) == 0 and time() - start_time < max_search_time and not self.stopped:
            self.tm.updateHaystack(self.screenshot)
            locs = self.tm.searchFor(needle, search_area=search_area, use_last_location=use_last_location, error_threshold=error_threshold)
            self.locations = locs
        return locs

    def findAllContours(self, color, search_area=None, max_search_time = float('inf'), area_threshold=50):
        locs = []
        start_time = time()
        while len(locs) == 0 and time() - start_time <= max_search_time and not self.stopped:
            self.cf.updateHaystack(self.screenshot)
            locs = self.cf.searchFor(color, search_area=search_area, area_threshold = area_threshold)
            self.locations = locs
        return locs

    def sortFastInv(self, locs):
        cols = []
        for loc in locs:
            if loc.left not in cols:
                cols.append(loc.left)
        cols.sort()
        inv = [[None for i in range(7)] for j in range(4)]
        r = 0
        prev_c = 0
        for loc in locs:
            c = cols.index(loc.left)
            if c < prev_c:
                r += 1
            inv[c][r] = loc
            prev_c = c
        retval = []
        for i in range(7):
            retval.append(inv[0][i])
            retval.append(inv[1][i])
        for i in range(7):
            retval.append(inv[2][i])
            retval.append(inv[3][i])
        return [x for x in retval if x is not None]