import sys
from collections import defaultdict


def neighbour_sum(d, i, j):
    return sum(d[(i + k, j + l)] for k in range(-1, 2) for l in range(-1, 2))


def answer(n):
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
    print(answer(int(sys.argv[1])))
