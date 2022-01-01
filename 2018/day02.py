import sys
from collections import Counter
from itertools import combinations


def load_data(path):
    with open(path) as f:
        return [line.strip() for line in f.readlines()]


def part_1(codes):
    n2, n3 = 0, 0

    for code in codes:
        counts = set(Counter(code).values())
        if 3 in counts:
            n3 += 1
        if 2 in counts:
            n2 += 1

    return n2 * n3


def diff(code1, code2):
    n = len(code1)
    return n - sum(c1 == c2 for c1, c2 in zip(code1, code2) if c1 == c2)


def part_2(codes):
    for code1, code2 in combinations(codes, 2):
        if diff(code1, code2) == 1:
            return "".join(c1 for c1, c2 in zip(code1, code2) if c1 == c2)


if __name__ == "__main__":
    codes = load_data(sys.argv[1])
    print(f"Part 1: {part_1(codes)}")
    print(f"Part 2: {part_2(codes)}")
