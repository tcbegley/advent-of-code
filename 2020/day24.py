import re
import sys
from collections import defaultdict

from tqdm.auto import tqdm

PATTERN = re.compile(r"ne|e|se|sw|w|nw")

DIRS = {
    "nw": (-1, -1),
    "ne": (-1, 0),
    "w": (0, -1),
    "e": (0, 1),
    "sw": (1, 0),
    "se": (1, 1),
}


def load_data(path):
    with open(path) as f:
        return [PATTERN.findall(s) for s in f.read().strip().split("\n")]


def get_neighbours(loc):
    for d in DIRS.values():
        yield (loc[0] + d[0], loc[1] + d[1])


def init_grid(directions):
    grid = defaultdict(lambda: False)

    for d in directions:
        steps = [DIRS[s] for s in d]
        loc = (sum(x[0] for x in steps), sum(x[1] for x in steps))
        grid[loc] = not grid[loc]

    return grid


def update_grid(grid):
    # only black tiles or tiles adjacent to black tiles can be flipped
    black = [k for k, v in grid.items() if v]
    possible = set()
    for k in black:
        possible.add(k)
        for nbr in get_neighbours(k):
            possible.add(nbr)

    new_black = []
    for tile in possible:
        nbrs = get_neighbours(tile)
        black_nbrs = sum(grid[nbr] for nbr in nbrs)
        tile_black = grid[tile]
        if tile_black and (black_nbrs == 1 or black_nbrs == 2):
            new_black.append(tile)
        elif not tile_black and black_nbrs == 2:
            new_black.append(tile)

    new_grid = defaultdict(lambda: False)
    for tile in new_black:
        new_grid[tile] = True

    return new_grid


def part_1(directions):
    return len([v for v in init_grid(directions).values() if v])


def part_2(directions, steps=100):
    grid = init_grid(directions)
    for i in tqdm(range(steps), leave=False):
        grid = update_grid(grid)

    return len([v for v in grid.values() if v])


if __name__ == "__main__":
    directions = load_data(sys.argv[1])
    print(f"Part 1: {part_1(directions)}")
    print(f"Part 2: {part_2(directions)}")
