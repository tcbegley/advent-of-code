import sys
from itertools import pairwise


def load_data(path):
    with open(path) as f:
        return [
            [int(i) for i in row.split(" ")] for row in f.read().strip().split("\n")
        ]


def is_safe(row):
    decreasing = row[0] > row[1]
    return all(
        (decreasing ^ (left < right)) and 1 <= abs(left - right) <= 3
        for left, right in pairwise(row)
    )


def part_1(data):
    return sum(is_safe(row) for row in data)


def part_2(data):
    return sum(
        any(is_safe(row[:i] + row[i + 1 :]) for i in range(len(row))) for row in data
    )


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
