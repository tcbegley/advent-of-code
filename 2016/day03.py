import re
import sys

NUMBERS = re.compile(r"\d+")


def load_data(path):
    with open(path) as f:
        return [[int(i) for i in NUMBERS.findall(line)] for line in f.readlines()]


def part_1(triangles):
    triangles = [sorted(t) for t in triangles]
    return sum(x + y > z for x, y, z in triangles)


def part_2(triangles):
    triangles = (
        [t[0] for t in triangles]
        + [t[1] for t in triangles]
        + [t[2] for t in triangles]
    )
    triangles = [
        sorted(triangles[3 * i : 3 * (i + 1)]) for i in range(len(triangles) // 3)
    ]
    return sum(x + y > z for x, y, z in triangles)


if __name__ == "__main__":
    triangles = load_data(sys.argv[1])
    print(f"Part 1: {part_1(triangles)}")
    print(f"Part 2: {part_2(triangles)}")
