import sys
from itertools import product


def load_data(path):
    with open(path) as f:
        return [tuple(map(int, row.split(","))) for row in f.read().strip().split("\n")]


def part_1(data):
    return max(
        (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        for (x1, y1), (x2, y2) in product(data, data)
    )


def part_2(data):
    pass


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
