import sys
from string import ascii_lowercase, ascii_uppercase

PRIORITIES = {
    c: i for i, c in enumerate(ascii_lowercase + ascii_uppercase, start=1)
}


def load_data(path):
    with open(path) as f:
        return f.read().strip().split("\n")


def part_1(data):
    total = 0
    for row in data:
        n = len(row)
        common = set(row[: n // 2]) & set(row[n // 2 :])
        total += PRIORITIES[next(iter(common))]

    return total


def part_2(data):
    total = 0
    for row1, row2, row3 in zip(*[iter(data)] * 3):
        badge = set(row1) & set(row2) & set(row3)
        total += PRIORITIES[next(iter(badge))]
    return total


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
