import re
import sys

DATA_PATTERN = re.compile(r"Step ([A-Z]).*step ([A-Z])")


def load_data(path):
    with open(path) as f:
        return [
            DATA_PATTERN.match(row).groups()
            for row in f.read().strip().split("\n")
        ]


def part_1(data):
    pass


def part_2(data):
    pass


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
