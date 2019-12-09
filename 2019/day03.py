import sys
from functools import reduce


def l1(vec):
    return reduce(lambda x, y: x + abs(y), vec, 0)


def get_locs(move, base):
    x, y = base
    d, steps = move[0], int(move[1:])

    if d in ("R", "L"):
        delta = 1 if d == "R" else -1
        return (
            [(x + (n + 1) * delta, y) for n in range(steps)],
            (x + steps * delta, y),
        )

    delta = 1 if d == "U" else -1
    return (
        [(x, y + (n + 1) * delta) for n in range(steps)],
        (x, y + steps * delta),
    )


def answer(path):
    with open(path) as f:
        wire1, wire2 = f.read().strip().split("\n")
        wire1 = wire1.strip().split(",")
        wire2 = wire2.strip().split(",")

    loc = (0, 0)
    locs1 = set()
    for move in wire1:
        locs, loc = get_locs(move, loc)
        locs1 = locs1.union(locs)

    loc = (0, 0)
    locs2 = set()
    for move in wire2:
        locs, loc = get_locs(move, loc)
        locs2 = locs2.union(locs)

    intersections = locs1 & locs2

    return l1(min(intersections, key=l1))


if __name__ == "__main__":
    print(answer(sys.argv[1]))
