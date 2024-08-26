import d3dshot
from pyscreeze import center
import win32gui
import numpy as np
from threading import Thread, Lock

from time import time
import cv2 as cv

class WindowCapture:
    # threading properties
    stopped = True
    lock = None
    screenshot = None
    # properties
    hwnd = None
    capture = None
    area = None

    def __init__(self, window_name=None):
        # create a thread lock object
        self.lock = Lock()
        # find the handle for the window we want to capture.
        # if no window name is given, capture the entire screen
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception("Window '{title}' not found.".format(title=window_name))
        self.capture = d3dshot.create(capture_output="numpy")
        self.setArea()

    def setArea(self):
        window_rect = win32gui.GetWindowRect(self.hwnd)

        display, area = WindowCapture.getDisplayArea(window_rect)

        #store
        self.display = display
        self.capture.display = self.capture.displays[display]
        self.area = area

    def updateScreenshot(self):
        # lock the thread while updating the data
        screenshot = self.capture.screenshot(region=self.area)
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    # threading methods
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        print("WC stoppping")
        self.stopped = True

    def run(self):
        while not self.stopped:
            self.updateScreenshot()
        print("WC stopped")

    @staticmethod
    def getDisplayArea(window_rect):
        left, top, right, bottom = window_rect
        width = right - left
        height = bottom - top
        centre_w = left + 250 # heuristic to determine which display the window is on. Useful when the window is only a few pixels on a diff screen
        # below is specific to my display setup and positions 1[1920,1080], 0[1920,1080], 2[1600,900]
        if centre_w < 0:
            display = 2
            left += 1920
        elif centre_w < 1920:
            display = 0
        else:
            display = 1
            left -= 1920
            top -= 169

        # account for the window border and titlebar and cut them off
        titlebar_pixels = 30
        border_pixels = 8
        top += titlebar_pixels
        left += border_pixels
        width -= border_pixels
        height -= border_pixels
        area = (left, top, left+width, top+height)
        return display, area

    @staticmethod
    def worldToWindowCoords(display, area, point):
        left, top, _, _ = area
        # below is specific to my display setup and positions 1[1920,1080], 0[1920,1080], 2[1600,900]
        if display == 2:
            left += 1920
        elif display == 1:
            left -= 1920
            top -= 169
        left += point[0]
        top += point[1]
        return (left, top-44)

    @staticmethod
    def windowToWorldCoors(display, area, point):
        left, top, _, _ = area
        # below is specific to my display setup and positions 1[1920,1080], 0[1920,1080], 2[1600,900]
        if display == 2:
            left -= 1920
        elif display == 1:
            left += 1920
            top += 169
        x, y = point
        return left+x, top+y

    @staticmethod
    def listWindowNames():
        def winEnumHandler(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                print(win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

if __name__=="__main__":
    wc = WindowCapture()
    wc.start()
    while True:
        lap = time()
        if wc.screenshot is None:
            continue
        lap = time()
        screenshot = wc.screenshot
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
        cv.imshow("Test Window", screenshot)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        print(f"Fps: {1/(time()-lap)}")
    cv.destroyAllWindows()
    wc.stop()
