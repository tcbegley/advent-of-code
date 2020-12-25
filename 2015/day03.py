import sys
from collections import defaultdict


def load_data(path):
    with open(path) as f:
        return f.read().strip()


def deliver(dirs):
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

    return houses


def part_1(dirs):
    return len(deliver(dirs))


def part_2(dirs):
    houses = deliver([d for i, d in enumerate(dirs) if i % 2 == 0])
    rhouses = deliver([d for i, d in enumerate(dirs) if i % 2 == 1])

    return len(set(houses.keys()) | set(rhouses.keys()))


if __name__ == "__main__":
    dirs = load_data(sys.argv[1])
    print(f"Part 1: {part_1(dirs)}")
    print(f"Part 2: {part_2(dirs)}")
