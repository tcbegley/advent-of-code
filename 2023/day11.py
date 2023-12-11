import sys
from itertools import combinations


def load_data(path):
    with open(path) as f:
        return [[char for char in row] for row in f.read().strip().split("\n")]


def locate_galaxies(grid, expand=2):
    row_map = [0] * len(grid)
    row = 0
    for r in range(len(grid)):
        row_map[r] = row
        if all(char == "." for char in grid[r]):
            row += expand
        else:
            row += 1

    col_map = [0] * len(grid[0])
    col = 0
    for c in range(len(grid[0])):
        col_map[c] = col
        if all(grid[r][c] == "." for r in range(len(grid))):
            col += expand
        else:
            col += 1

    return [
        (row_map[r], col_map[c])
        for r, row in enumerate(grid)
        for c, char in enumerate(row)
        if char == "#"
    ]


def l1(g1, g2):
    return abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])


def part_1(grid):
    return sum(l1(g1, g2) for g1, g2 in combinations(locate_galaxies(grid), 2))


def part_2(grid):
    return sum(
        l1(g1, g2)
        for g1, g2 in combinations(locate_galaxies(grid, expand=1_000_000), 2)
    )


if __name__ == "__main__":
    grid = load_data(sys.argv[1])
    print(f"Part 1: {part_1(grid)}")
    print(f"Part 2: {part_2(grid)}")
