import sys
from collections import defaultdict


def answer(path):
    with open(path) as f:
        dirs = f.read().strip()

    houses = defaultdict(lambda: 0)
    rhouses = defaultdict(lambda: 0)

    x, y, rx, ry = 0, 0, 0, 0

    houses[(0, 0)] += 1
    rhouses[(0, 0)] += 1

    for i, d in enumerate(dirs):
        if i % 2 == 0:
            if d == "^":
                y += 1
            elif d == "v":
                y -= 1
            elif d == ">":
                x += 1
            elif d == "<":
                x -= 1
            houses[(x, y)] += 1
        else:
            if d == "^":
                ry += 1
            elif d == "v":
                ry -= 1
            elif d == ">":
                rx += 1
            elif d == "<":
                rx -= 1
            rhouses[(rx, ry)] += 1

    return len(set(houses.keys()) | set(rhouses.keys()))


if __name__ == "__main__":
    print(answer(sys.argv[1]))
