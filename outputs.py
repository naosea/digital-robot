import numpy as np
from bezier import Curve
from pytweening import easeInOutQuad, easeOutBack
import pyautogui as pag

from windowcapture import WindowCapture

from utils import wait, getGaussianDeviation
from math import log2

pag.PAUSE = 0.001
OS_SPEED = 60

class MouseController:
    reaction_time = 0.1

    # constructor
    def __init__(self, debug=False):
        self.debug = debug

    def click(self, right_click = False, shift = False):
        delay = self.reaction_time
        spread = delay / 2
        if shift:
            pag.keyDown("shift")
        wait(delay/3, spread = spread/3)
        if right_click:
            pag.mouseDown(button="right")
            wait(delay/3, spread = spread/3)
            pag.mouseUp(button="right")
        else:
            pag.mouseDown(button="left")
            wait(delay/3, spread = spread/3)
            pag.mouseUp(button="left")
        wait(delay/3, spread = spread/3)
        if shift:
            pag.keyUp("shift")

    def press(self, key):
        if self.debug:
            print(f"Pressing {key}")
        delay = self.reaction_time
        spread = delay / 2
        wait(delay/3, spread = spread/3)
        try:
            pag.keyDown(key)
            wait(delay/3, spread = spread/3)
            pag.keyUp(key)
        except:
            print(f"Invalid key: {key}.")
        wait(delay/3, spread = spread/3)

    def hold(self, key):
        delay = self.reaction_time
        spread = delay / 2
        wait(delay/2, spread = spread/2)
        try:
            pag.keyDown(key)
        except:
            print(f"Invalid key: {key}.")
        wait(delay/2, spread = spread/2)

    def release(self, key):
        delay = self.reaction_time
        spread = delay / 2
        wait(delay/2, spread = spread/2)
        try:
            pag.keyUp(key)
        except:
            print(f"Invalid key: {key}.")
        wait(delay/2, spread = spread/2)

    def move(self, target, display, window_coords, fast=False):
        steps = self.calcPath(target, display, window_coords, fast=fast)
        if steps.T.shape[0] == 0:
            return
        if self.debug:
            dest = steps.T[-1]
            print(f"Moving to: {dest}")
        for step in steps.T:
            pag.moveTo(step[0], step[1])

    def calcPath(self, target, display, window_coords, fast=False):
        origin = pag.position()
        test_origin = WindowCapture.worldToWindowCoords(display, window_coords, origin)
        if target.isPointWithin(test_origin):
            return np.empty(0)
        dest = target.getPointWithin()
        dest = WindowCapture.windowToWorldCoors(display, window_coords, dest)
        vector = tuple(np.subtract(dest, origin))
        distance = np.sqrt(vector[0] ** 2 + vector[1] ** 2)

        anchors_x = [origin[0]]
        anchors_y = [origin[1]]
        anchor_x = origin[0] + (vector[0] / 2)
        anchor_y = origin[1] + (vector[1] / 2)
        anchor_x = int(anchor_x + getGaussianDeviation(distance * 0.75))
        anchor_y = int(anchor_y + getGaussianDeviation(distance * 0.75))
        anchors_x.append(anchor_x)
        anchors_y.append(anchor_y)
        anchors_x.append(dest[0])
        anchors_y.append(dest[1])

        anchors = np.array([
            np.asarray(anchors_x, np.float),
            np.asarray(anchors_y, np.float)
        ])

        curve = Curve(anchors, degree = 2)

        a = 0.10
        b = 0.10
        if fast:
            a = a/2
            b = b/2
        fitts_width = (target.width + target.height) / 2
        fitts_time = a + b * log2((distance/fitts_width) + 1)
        #print(fitts_time)
        poll = int(OS_SPEED * fitts_time)
        vals = np.linspace(0, 1, poll)

        tweenedVals = []

        overshoot = abs(getGaussianDeviation(1.5, integer = False))
        for v in vals:
            tweenedVal = easeInOutQuad(v)
            tweenedVal = easeOutBack(tweenedVal, overshoot)
            tweenedVals.append(tweenedVal)
        points = curve.evaluate_multi(np.array(tweenedVals))
        return points