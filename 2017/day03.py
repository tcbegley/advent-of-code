import sys
from collections import defaultdict
from math import sqrt


def load_data(path):
    with open(path) as f:
        return int(f.read().strip())


def neighbour_sum(d, i, j):
    return sum(d[(i + x, j + y)] for x in range(-1, 2) for y in range(-1, 2))


def part_1(n):
    lookup = [0, 0]
    limit = (int(sqrt(n - 1)) + 1) // 2 + 1
    for i in range(1, limit):
        lookup.extend(
            (list(range(2 * i - 1, i - 1, -1)) + list(range(i + 1, 2 * i + 1))) * 4
        )
    return lookup[n]


def part_2(n):
    top = 1
    d = defaultdict(lambda: 0)
    d[(0, 0)] = 1
    i = 1
    while top < n:
        # right hand column
        for j in range(2 * i):
            d[(i, 1 - i + j)] = neighbour_sum(d, i, 1 - i + j)
        # top row
        for j in range(2 * i):
            d[(i - 1 - j, i)] = neighbour_sum(d, i - 1 - j, i)
        # left hand column
        for j in range(2 * i):
            d[(-i, i - 1 - j)] = neighbour_sum(d, -i, i - 1 - j)
        # bottom row
        for j in range(2 * i):
            d[(-i + 1 + j, -i)] = neighbour_sum(d, -i + 1 + j, -i)
        top = max(d.values())
        i += 1
    # want first time n is exceeded, i.e. smallest value larger than n
    # guaranteed to work since monotone sequence.
    return min(m for m in d.values() if m >= n)


if __name__ == "__main__":
    n = load_data(sys.argv[1])
    print(f"Part 1: {part_1(n)}")
    print(f"Part 2: {part_2(n)}")
