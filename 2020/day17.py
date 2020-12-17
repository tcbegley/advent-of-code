import sys
from collections import defaultdict
from itertools import product


def load_data(path):
    with open(path) as f:
        lines = f.read().strip().split("\n")

    grid = defaultdict(lambda: ".")

    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == "#":
                grid[(i, j, 0)] = c

    return grid


def get_neighbours3(loc):
    for dx, dy, dz in product(*[[-1, 0, 1]] * 3):
        if dx == 0 and dy == 0 and dz == 0:
            continue
        yield (loc[0] + dx, loc[1] + dy, loc[2] + dz)


def get_neighbours4(loc):
    for dx, dy, dz, dw in product(*[[-1, 0, 1]] * 4):
        if dx == 0 and dy == 0 and dz == 0 and dw == 0:
            continue
        yield (loc[0] + dx, loc[1] + dy, loc[2] + dz, loc[3] + dw)


def step(grid, get_neighbours):
    active = [k for k, v in grid.items() if v == "#"]

    # only neighbours of active cells could be active next time
    possible = []
    for cell in active:
        possible.append(cell)
        possible.extend(get_neighbours(cell))
    possible = set(possible)

    new_active = []
    for cell in possible:
        nbrs = get_neighbours(cell)
        active_nbrs = sum(grid[nbr] == "#" for nbr in nbrs)
        cell_active = grid[cell] == "#"
        if (cell_active and active_nbrs == 2) or active_nbrs == 3:
            new_active.append(cell)

    new_grid = defaultdict(lambda: ".")
    for cell in new_active:
        new_grid[cell] = "#"

    return new_grid


def part_1(grid):
    for _ in range(6):
        grid = step(grid, get_neighbours3)

    return sum(v == "#" for v in grid.values())


def part_2(grid):
    old_grid = grid
    grid = defaultdict(lambda: ".")
    for loc, v in old_grid.items():
        grid[(loc[0], loc[1], loc[2], 0)] = v

    for _ in range(6):
        grid = step(grid, get_neighbours4)

    return sum(v == "#" for v in grid.values())


if __name__ == "__main__":
    grid = load_data(sys.argv[1])
    print(f"Part 1: {part_1(grid)}")
    print(f"Part 2: {part_2(grid)}")
