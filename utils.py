from random import gauss
from time import sleep

def wait(secs, spread = 0.05):
    # will sleep for between secs-spread and secs+spread
    secs = max(0, secs)
    spread = abs(spread / 5)
    t = secs + gauss(0, 1) * spread
    t = max(0, t)
    sleep(t)
    return t

def waitAtLeast(secs, spread = 0.05):
    # will sleep for between secs and secs+spread
    secs = max(0, secs)
    spread = abs(spread / 5)
    t = secs + abs(gauss(0, 1) * spread)
    sleep(t)
    return t

def getGaussianDeviation(radius, integer = True):
    v = float('inf')
    while v > radius:
        v = gauss(0, 1) * radius/3
    return v if not integer else round(v)