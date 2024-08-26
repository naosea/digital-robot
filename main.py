from time import time
import cv2 as cv
import numpy as np

from windowcapture import WindowCapture

from scripts.testbot import *
from scripts.cooking import *
from scripts.sandstone import *
from scripts.herbcleaning import *
from scripts.mythcaper import *
from scripts.ironminer import *
from scripts.cookkarabwans import *
from scripts.blastfurnace import *
from scripts.fletchbroads import *
from scripts.zmileagues import *
from scripts.stunalch import *
from scripts.cutdiamonds import *
from scripts.monkeylaps import *
from scripts.firemaking import *
from scripts.ardylaps import *

class Bot:
    wc = WindowCapture("RuneLite")
    stopped = False
    scripts = [None]
    clicks=[]

    def __init__(self, debug=True):
        self.debug = debug
        self.scripts.append(TestBot)
        self.scripts.append(Cooker)
        self.scripts.append(Sandstoner)
        self.scripts.append(HerbCleaner)
        self.scripts.append(MythCaper)
        self.scripts.append(IronMiner)
        self.scripts.append(CookKarabwan)
        self.scripts.append(BlastFurnace)
        self.scripts.append(FletchBroads)
        self.scripts.append(ZMILeagues)
        self.scripts.append(StunAlcher)
        self.scripts.append(CutDiamonds)
        self.scripts.append(MonkeyLaps)
        self.scripts.append(Firemaking)
        self.scripts.append(ArdyLaps)

    def start(self):
        self.printMenu()
        script_number = self.getMenuChoice()
        if script_number == 0:
            return False
        self.script = self.getScript(script_number)
        print(f"Running script {type(self.script)}")
        self.script.display = self.wc.display
        self.script.window_coords = self.wc.area
        self.wc.start()
        while self.wc.screenshot is None:
            pass
        self.script.updateScreenshot(self.wc.screenshot)
        self.script.start()
        if self.debug:
            #self.script.mc.debug = True
            cv.namedWindow("Debug Window")
            cv.setMouseCallback("Debug Window", self.onMouse)
        return True

    def stop(self):
        self.stopped = True
        self.wc.stop()
        self.script.stop()
        if self.debug:
            cv.destroyAllWindows()

    def run(self):
        if self.script is None:
            self.stop()
        frames = 0
        lap = time()
        while not self.stopped:
            screenshot = self.wc.screenshot
            #self.script.updateScreenshot(np.copy(screenshot))
            self.script.screenshot = screenshot
            if self.debug:
                self.debugDisplay(screenshot)
                frames += 1
                if frames >= 100:
                    print(f"fps: {frames/(time()-lap)}")
                    frames = 0
                    lap = time()

    def debugDisplay(self, screenshot):
        screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
        for i, area in enumerate(self.script.search_areas):
            left, top, right, bottom = area.getBounds()
            cv.rectangle(screenshot, pt1=(left, top), pt2=(right, bottom), color=(0, 255, 0), lineType=cv.LINE_4, thickness=1)
            cv.putText(screenshot, self.script.search_area_names[i], (left, top+25), 0, 1, (0, 255, 0))
        for i, loc in enumerate(self.script.locations):
            if loc.contour is None:
                left, top, right, bottom = loc.getBounds()
                cv.rectangle(screenshot, pt1=(left, top), pt2=(right, bottom), color=(0, 255, 0), lineType=cv.LINE_4, thickness=1)
                cv.putText(screenshot, str(i+1), (left, top+25), 0, 1, (0, 255, 0))
            else:
                rect = cv.minAreaRect(loc.contour)
                box = cv.boxPoints(rect)
                box = np.int0(box)
                cv.drawContours(screenshot, [box], 0, (0, 255, 0), 1)
        screenshot = cv.resize(screenshot, None, fx = 0.5, fy = 0.5)
        cv.imshow("Debug Window", screenshot)
        if cv.waitKey(1) & 0xFF == ord('q'):
            self.stop()

    def onMouse(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDBLCLK:
            print(f"Click recorded at: {x}, {y}")
            self.clicks.append((x,y))

    def printMenu(self):
        print()
        print("Script Menu.")
        print("0. Quit")
        for i, script in enumerate(self.scripts[1:]):
            print(f"{i+1}. {script.__name__}")
        print()

    def getMenuChoice(self):
        valid = False
        choice = -1
        while not valid:
            try:
                choice = int(input("Enter script num: "))
                print()
            except ValueError:
                print("Please enter an int")
                print()
            if 0 <= choice <= len(self.scripts)-1:
                valid = True
            else:
                print("Please enter a valid int")
                print()
        return choice

    def getScript(self, script_number):
        return self.scripts[script_number]()

def main():
    bot = Bot()
    if not bot.start():
        print("Quitting.")
        return
    try:
        bot.run()
    except KeyboardInterrupt:
        print("Stopping by interupt")
        bot.stop()
    print(bot.clicks)

if __name__=="__main__":
    main()
    exit()