import re
import sys

NUMBERS = re.compile(r"\d+")


def load_data(path):
    with open(path) as f:
        return map(int, NUMBERS.findall(f.read().strip()))


def part_1(x, y):
    n = (y + x - 1) * (y + x) // 2 - x

    code = 20151125
    for _ in range(n):
        code = (code * 252533) % 33554393

    return code


if __name__ == "__main__":
    x, y = load_data(sys.argv[1])
    print(f"Part 1: {part_1(x, y)}")
