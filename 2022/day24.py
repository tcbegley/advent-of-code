import sys
from collections import deque
from dataclasses import dataclass
from functools import cache

# coords are (row, col)
DIR_LOOKUP = {">": (0, 1), "^": (-1, 0), "<": (0, -1), "v": (1, 0)}


@dataclass(frozen=True)
class Blizzard:
    location: tuple[int, int]
    direction: tuple[int, int]


def get_grid_factory(blizzards, n_rows, n_cols):
    @cache
    def get_grid(time):
        return {
            (
                (b.location[0] + time * b.direction[0]) % n_rows,
                (b.location[1] + time * b.direction[1]) % n_cols,
            ): b.direction
            for b in blizzards
        }

    return get_grid


def load_data(path):
    with open(path) as f:
        rows = f.read().strip().split("\n")

    n_rows = len(rows) - 2
    n_cols = len(rows[0]) - 2

    blizzards = [
        Blizzard((r, c), DIR_LOOKUP[char])
        for r, row in enumerate(rows[1:-1])
        for c, char in enumerate(row[1:-1])
        if char in "<>^v"
    ]
    return (
        blizzards,
        (-1, rows[0].index(".") - 1),
        (n_rows, rows[-1].index(".") - 1),
        n_rows,
        n_cols,
    )


def get_neighbours(loc, n_rows, n_cols, start, end):
    r, c = loc
    for dr, dc in ((-1, 0), (1, 0), (0, 0), (0, -1), (0, 1)):
        nbr = nr, nc = r + dr, c + dc
        if nbr in (start, end) or (0 <= nr < n_rows and 0 <= nc < n_cols):
            yield nbr


def bfs(blizzards, start, end, n_rows, n_cols, time_offset=0):
    queue = deque([(0, start)])
    get_grid = get_grid_factory(blizzards, n_rows, n_cols)

    seen = {(0, start)}

    while queue:
        steps, loc = queue.popleft()

        if loc == end:
            return steps

        grid = get_grid(time_offset + steps + 1)

        for nbr in get_neighbours(loc, n_rows, n_cols, start, end):
            if nbr not in grid and (steps + 1, nbr) not in seen:
                seen.add((steps + 1, nbr))
                queue.append((steps + 1, nbr))


def part_1(blizzards, start, end, n_rows, n_cols):
    return bfs(blizzards, start, end, n_rows, n_cols)


def part_2(blizzards, start, end, n_rows, n_cols):
    t1 = bfs(blizzards, start, end, n_rows, n_cols)
    t2 = bfs(blizzards, end, start, n_rows, n_cols, time_offset=t1)
    return (
        t1
        + t2
        + bfs(blizzards, start, end, n_rows, n_cols, time_offset=t1 + t2)
    )


if __name__ == "__main__":
    blizzards, start, end, n_rows, n_cols = load_data(sys.argv[1])
    print(f"Part 1: {part_1(blizzards, start, end, n_rows, n_cols)}")
    print(f"Part 2: {part_2(blizzards, start, end, n_rows, n_cols)}")
