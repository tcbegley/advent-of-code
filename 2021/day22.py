import re
import sys
from collections import defaultdict

NUMBER_PATTERN = re.compile(r"\-?[0-9]+")


def load_data(path):
    def process_line(line):
        on, coords = line.split(" ")
        coords = NUMBER_PATTERN.findall(coords)
        return on == "on", tuple(int(i) for i in coords)

    with open(path) as f:
        return [process_line(line) for line in f.readlines()]


def size(cube):
    x0, x1, y0, y1, z0, z1 = cube
    return max(x1 - x0 + 1, 0) * max(y1 - y0 + 1, 0) * max(z1 - z0 + 1, 0)


def intersection(c1, c2):
    return (
        max(c1[0], c2[0]),
        min(c1[1], c2[1]),
        max(c1[2], c2[2]),
        min(c1[3], c2[3]),
        max(c1[4], c2[4]),
        min(c1[5], c2[5]),
    )


def answer(data):
    # keep track of cubes seen so far and a count
    cubes = defaultdict(int)

    # iteratively build up the terms in this formula:
    # https://proofwiki.org/wiki/Cardinality_of_Set_Union#General_Case
    for on, cube in data:
        # intersect each new cube with all previous cubes and intersections of
        # previous cubes, then subtract that from the total (use the count to)
        # track multiplicities
        for other, count in list(cubes.items()):
            i = intersection(cube, other)
            if size(i) > 0:
                cubes[i] -= count

        # each new cube gets added to the set of cubes with multiplicity 1
        if on:
            cubes[cube] += 1

    # result is sum of weighted sizes of the cubes
    return sum(size(cube) * count for cube, count in cubes.items())


def part_1(data):
    data = [(on, intersection(cube, (-50, 50) * 3)) for on, cube in data]
    data = [(on, cube) for on, cube in data if size(cube) > 0]
    return answer(data)


def part_2(data):
    return answer(data)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
