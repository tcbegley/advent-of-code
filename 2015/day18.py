import sys
from itertools import product

from tqdm.auto import tqdm


def load_data(path):
    with open(path) as f:
        grid = f.read().strip().split("\n")

    return {
        (x, y): c == "#"
        for y, row in enumerate(grid)
        for x, c in enumerate(row)
    }


def get_neighbours(loc, max_x, max_y):
    for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
        if dx == 0 and dy == 0:
            continue
        x, y = loc[0] + dx, loc[1] + dy

        if 0 <= x <= max_x and 0 <= y <= max_y:
            yield x, y


def animate_step(grid, max_x, max_y, pin_corners):
    new_grid = {}
    for loc, on in grid.items():
        if pin_corners:
            if loc in ((0, 0), (0, max_y), (max_x, 0), (max_x, max_y)):
                new_grid[loc] = True
                continue
        on_nbrs = sum(grid[nbr] for nbr in get_neighbours(loc, max_x, max_y))
        new_grid[loc] = on_nbrs == 3 or (on and on_nbrs == 2)

    return new_grid


def animate(grid, pin_corners=False):
    max_x = max(x for x, _ in grid)
    max_y = max(y for _, y in grid)

    if pin_corners:
        grid[(0, 0)] = True
        grid[(0, max_y)] = True
        grid[(max_x, 0)] = True
        grid[(max_x, max_y)] = True

    for _ in tqdm(range(100), leave=False):
        grid = animate_step(grid, max_x, max_y, pin_corners)

    return sum(grid.values())


def part_1(grid):
    return animate(grid)


def part_2(grid):
    # return grid
    return animate(grid, pin_corners=True)


if __name__ == "__main__":
    grid = load_data(sys.argv[1])
    print(f"Path 1: {part_1(grid)}")
    print(f"Path 2: {part_2(grid)}")
