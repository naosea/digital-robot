from mouse import play, record, hook, unhook
from keyboard import wait

def main():
    print('Recording... Double click to stop and replay.')
    events = []
    hook(events.append)   #starting the recording
    wait("a")          #Waiting for 'a' to be pressed
    unhook(events.append)
    play(events, speed_factor=0)

def sortFastInv(locs):
    cols = []
    for loc in locs:
        if loc[1] not in cols:
            cols.append(loc[1])
    cols.sort()
    inv = [[None for i in range(8)] for j in range(4)]
    r = 0
    for loc in locs:
        c = cols.index(loc[1])
        inv[c][r] = loc
        if c == len(cols)-1:
            r += 1
    retval = []
    for i in range(8):
        retval.append(inv[0][i])
        retval.append(inv[1][i])
    for i in range(8):
        retval.append(inv[2][i])
        retval.append(inv[3][i])
    return [x for x in retval if x is not None]

if __name__ == '__main__':
    locs = [(1, 2), (1, 3), (1, 4),
            (2, 2), (2, 3), (2, 4),
            (3, 2), (3, 3), (3, 4),
            (4, 2), (4, 3), (4, 4),
            (5, 2), (5, 3), (5, 4),
            (6, 2), (6, 3), (6, 4),
            (7, 2), (7, 3), (7, 4),
            (8, 2), (8, 3), (8, 4)]
    locs = sortFastInv(locs)
    print(locs)