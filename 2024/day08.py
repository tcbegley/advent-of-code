import sys
from itertools import combinations


def load_data(path):
    with open(path) as f:
        rows = f.read().strip().split("\n")

    n_rows = len(rows)
    n_cols = len(rows[0])

    antennae = {}
    for r, row in enumerate(rows):
        for c, char in enumerate(row):
            if char != ".":
                antennae.setdefault(char, []).append(r + c * 1j)
    return antennae, n_rows, n_cols


def in_bounds(loc, n_rows, n_cols):
    return 0 <= loc.real < n_rows and 0 <= loc.imag < n_cols


def add_antinodes_1(antinodes, loc1, loc2, diff, n_rows, n_cols):
    if in_bounds(loc := loc1 - diff, n_rows, n_cols):
        antinodes.add(loc)
    if in_bounds(loc := loc2 + diff, n_rows, n_cols):
        antinodes.add(loc)


def add_antinodes_2(antinodes, loc1, loc2, diff, n_rows, n_cols):
    n = 0
    while in_bounds(loc := loc1 - n * diff, n_rows, n_cols):
        antinodes.add(loc)
        n += 1

    n = 0
    while in_bounds(loc := loc2 + n * diff, n_rows, n_cols):
        antinodes.add(loc)
        n += 1


def count_antinodes(antennae, n_rows, n_cols, part_2=False):
    antinodes = set()

    for locs in antennae.values():
        for loc1, loc2 in combinations(locs, 2):
            diff = loc2 - loc1
            if part_2:
                add_antinodes_2(antinodes, loc1, loc2, diff, n_rows, n_cols)
            else:
                add_antinodes_1(antinodes, loc1, loc2, diff, n_rows, n_cols)
    return len(antinodes)


def part_1(antennae, n_rows, n_cols):
    return count_antinodes(antennae, n_rows, n_cols)


def part_2(antennae, n_rows, n_cols):
    return count_antinodes(antennae, n_rows, n_cols, part_2=True)


if __name__ == "__main__":
    antennae, n_rows, n_cols = load_data(sys.argv[1])
    print(f"Part 1: {part_1(antennae, n_rows, n_cols)}")
    print(f"Part 2: {part_2(antennae, n_rows, n_cols)}")
