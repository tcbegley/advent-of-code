import sys


def coordinate(steps):
    lookup = {
        "n": (0, 1),
        "s": (0, -1),
        "ne": (1, 0),
        "nw": (-1, 1),
        "se": (1, -1),
        "sw": (-1, 0),
    }
    pos = [0, 0]
    for step in steps:
        pos[0] += lookup[step][0]
        pos[1] += lookup[step][1]
    return pos


def answer(file_path):
    with open(file_path, "r") as f:
        steps = f.read().strip().split(",")
    pos = coordinate(steps)
    if pos[0] * pos[1] > 0:
        return abs(pos[0]) + abs(pos[1])
    return max(abs(pos[0]), abs(pos[1]))


if __name__ == "__main__":
    print(answer(sys.argv[1]))
