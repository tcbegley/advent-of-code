import sys

import numpy as np


def get_power_level(x, y, s):
    rid = x + 10
    pl = rid * y
    pl += s
    pl *= rid
    pl = (pl % 1000) // 100
    return pl - 5


def get_best(grid, s):
    best = -float("inf")
    bestx = None
    besty = None

    for x in range(301 - s):
        for y in range(301 - s):
            total = grid[x : x + s, y : y + s].sum()
            if total > best:
                best = total
                bestx = x
                besty = y

    return bestx, besty, best


def answer(serial_no):
    grid = np.zeros((300, 300))

    for i in range(300):
        for j in range(300):
            grid[i, j] = get_power_level(i, j, serial_no)

    best = -float("inf")
    bestx = None
    besty = None
    bests = None

    for s in range(1, 301):
        print(s)
        x, y, total = get_best(grid, s)
        if total > best:
            bestx = x
            besty = y
            bests = s
            best = total

    return bestx, besty, bests


if __name__ == "__main__":
    print(answer(int(sys.argv[1])))
