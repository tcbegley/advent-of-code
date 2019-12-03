import sys
from collections import defaultdict


def answer(path):
    with open(path) as f:
        dirs = f.read().strip()

    houses = defaultdict(lambda: 0)

    x, y = 0, 0
    houses[(0, 0)] += 1

    for d in dirs:
        if d == "^":
            y += 1
        elif d == "v":
            y -= 1
        elif d == ">":
            x += 1
        elif d == "<":
            x -= 1
        houses[(x, y)] += 1

    return len(houses)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
