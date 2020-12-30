import sys

LOOKUP = {
    "n": (0, 1),
    "s": (0, -1),
    "ne": (1, 0),
    "nw": (-1, 1),
    "se": (1, -1),
    "sw": (-1, 0),
}


def load_data(path):
    with open(path) as f:
        return f.read().strip().split(",")


def coordinate(steps):
    x, y = 0, 0
    for step in steps:
        x += LOOKUP[step][0]
        y += LOOKUP[step][1]
        yield x, y


def distance(loc):
    if loc[0] * loc[1] > 0:
        return abs(loc[0]) + abs(loc[1])
    return max(abs(loc[0]), abs(loc[1]))


def part_1(steps):
    loc = list(coordinate(steps))[-1]
    return distance(loc)


def part_2(steps):
    return max(distance(loc) for loc in coordinate(steps))


if __name__ == "__main__":
    steps = load_data(sys.argv[1])
    print(f"Part 1: {part_1(steps)}")
    print(f"Part 2: {part_2(steps)}")
