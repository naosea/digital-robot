from bot import Script
from needle import Needle
from region import Region
from utils import wait, waitAtLeast

class IronMiner(Script):

    def __init__(self):
        super().__init__()
        self.start_up = True
        self.search_areas = []
        self.search_area_names = []

    def startUp(self):
        self.full_inv_check = Needle('ironmining/full_inv_check.png', transparent=True)
        self.iron_inv = Needle('ironmining/iron_inv.png', transparent=True)
        self.sapphire = Needle('ironmining/sapphire.png', transparent=False)
        r1 = Needle('ironmining/r1.png', transparent=False)
        r2 = Needle('ironmining/r2.png', transparent=False)
        r3 = Needle('ironmining/r3.png', transparent=False)
        self.rocks = [r1, r2, r3]
        r1g = Needle('ironmining/r1g.png', transparent=False)
        r2g = Needle('ironmining/r2g.png', transparent=False)
        r3g = Needle('ironmining/r3g.png', transparent=False)
        self.rocks_gone = [r1g, r2g, r3g]
        self.rock_number = 0

    def nextRock(self):
        next = self.rock_number
        if next == 0:
            new = 1
        elif next == 1:
            new = 2
        elif next == 2:
            new = 0
        return new

    def main(self):
        if self.start_up:
            self.startUp()
            self.start_up = False
        #if self.find(self.full_inv_check, max_search_time=0.1) is not None:
        self.mine()
        #else:
        #    self.drop()

    def drop(self):
        iron_locs = self.findAll(self.iron_inv)
        iron_locs = self.sortFastInv(iron_locs)
        self.clickAll(iron_locs, shift=True, fast=True)
        sapphires = self.findAll(self.sapphire, max_search_time=0.1)
        self.clickAll(sapphires, shift=True, fast=True)

    def mine(self):
        self.clickIn(self.find(self.rocks[self.rock_number]))
        next = self.nextRock()
        self.moveInto(self.rocks[next].last_location)
        self.find(self.rocks_gone[self.rock_number])
        self.rock_number = next