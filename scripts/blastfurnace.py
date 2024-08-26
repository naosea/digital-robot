from bot import Script
from needle import Needle
from region import Region
from utils import wait, waitAtLeast

class BlastFurnace(Script):

    def __init__(self):
        super().__init__()
        self.start_up = True

    def startUp(self):
        self.deposit = Needle('common/deposit.png', transparent=False)
        self.confirm = Needle('blastfurnace/confirm.png', transparent=False)
        self.dispenser = Needle('blastfurnace/dispenser.png', transparent=True)
        self.empty_inv = Needle('blastfurnace/empty_inv.png', transparent=False)
        self.gold_bank = Needle('blastfurnace/gold_bank.png', transparent=False)
        self.red = self.find("red")
        self.green = self.find("green")
        self.cyan = self.find("cyan")
        self.magenta = self.find("magenta")

    def main(self):
        if self.start_up:
            self.startUp()
            self.start_up = False
        self.clickIn(self.find(self.deposit))
        self.clickIn(self.find(self.gold_bank))
        self.press("esc")
        self.clickIn(self.red)
        self.moveInto(self.green)
        self.find(self.empty_inv)
        self.clickIn(self.green)
        self.moveInto(self.cyan)
        wait(4.5)
        self.find(self.dispenser)
        self.clickIn(self.cyan)
        while self.find(self.confirm, max_search_time=0.8) is None:
            self.clickIn(self.cyan)
        self.press("space")
        self.clickIn(self.magenta)
        self.moveInto(self.deposit.last_location)