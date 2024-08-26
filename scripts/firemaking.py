from bot import Script
from needle import Needle
from region import Region
from utils import wait, waitAtLeast

class Firemaking(Script):

    def __init__(self):
        super().__init__()
        self.start_up = True

    def startUp(self):
        self.logs_bank = Needle('firemaking/logs_bank.png', transparent=False)
        self.logs_inv = Needle('firemaking/logs_inv.png', transparent=False)
        self.tinderbox = Needle('firemaking/tinderbox.png', transparent=False)
        self.teleport = Needle('firemaking/teleport.png', transparent=False)
        self.red = self.find("red")
        self.cyan = self.find("cyan")
        self.row = 0
        self.logortinder = 0

    def main(self):
        if self.start_up:
            self.startUp()
            self.start_up = False
        self.bank()
        waitAtLeast(1.5)
        self.firemake()

    def bank(self):
        self.clickIn(self.find("magenta"))
        self.clickIn(self.find(self.logs_bank))
        if self.row == 0:
            self.clickIn(self.red)
            self.row = 1
        else:
            self.clickIn(self.cyan)
            self.row = 0
        waitAtLeast(0.6)
        self.press("esc")

    def firemake(self):
        logs = self.findAll(self.logs_inv)
        self.clickIn(self.find(self.tinderbox), fast=True)
        self.clickIn(logs[0], fast=True)
        waitAtLeast(1.2)
        for log in logs[1:]:
            self.clickIn(self.find(self.tinderbox), fast=True)
            self.moveInto(log, fast=True)
            waitAtLeast(1.8)
            self.clickIn(log, fast=True)
        self.press("f3")
        waitAtLeast(1.8)
        self.clickIn(self.find(self.teleport))