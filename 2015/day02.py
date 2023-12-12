import sys
from itertools import combinations


def load_data(path):
    with open(path) as f:
        return [
            [int(i) for i in line.split("x")] for line in f.read().strip().split("\n")
        ]


def required1(dim):
    areas = [a * b for a, b in combinations(dim, 2)]
    return 2 * sum(areas) + min(areas)


def required2(dim):
    a, b, c = sorted(dim)
    return 2 * (a + b) + a * b * c


def part_1(dims):
    return sum(map(required1, dims))


def part_2(dims):
    return sum(map(required2, dims))


if __name__ == "__main__":
    dims = load_data(sys.argv[1])
    print(f"Part 1: {part_1(dims)}")
    print(f"Part 2: {part_2(dims)}")
