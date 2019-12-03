import sys
from itertools import combinations


def required(dim):
    areas = [a * b for a, b in combinations(dim, 2)]
    return 2 * sum(areas) + min(areas)


def answer(path):
    with open(path) as f:
        dims = [
            [int(i) for i in line.split("x")]
            for line in f.read().strip().split("\n")
        ]

    return sum(required(dim) for dim in dims)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
