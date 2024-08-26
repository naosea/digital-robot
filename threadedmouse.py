    # constructor
    def __init__(self):
        self.lock = Lock()

    def updateTarget(self, target, fast=False):
        if target != self.target:
            self.lock.acquire()
            self.target = target
            self.lock.release()
            path = self.calcPath(fast=fast)
            self.updatePath(path)

    def updatePath(self, path):
        self.lock.acquire()
        self.path = path
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self._run)
        t.start()

    def stop(self):
        self.stopped = True

    def _run(self):
        while not self.stopped and len(self.path[0]) != 0:
            if self.target is None:
                continue
            else:
                next_x = round(self.path[0][0])
                next_y = round(self.path[1][0])
                pag.moveTo(next_x, next_y)
                remainder_x = self.path[0][1:]
                remainder_y = self.path[0][1:]
                remainder_path = [remainder_x, remainder_y]
                self.updatePath(remainder_path)

    def isMouseIn(self, region):
        x, y = pag.position()
        return region.isPointWithin((x, y))



def clickIn(region, rightClick = False, shift = False, fast = False):
    if not region:
        raise Exception("No region given")
    if not isMouseIn(region):
        moveInto(region, fast = fast)
    return click(rightClick = rightClick, shift = shift)

def clickAll(locations, shift = False, fast = False):
    for location in locations:
        clickIn(location, shift = shift, fast = fast)
        wait(0) # ?

def moveInto(region, fast = False):
    if not region:
        return
    if isMouseIn(region):
        return
    dest = region.getPointWithin()
    move(dest, fast = fast)

