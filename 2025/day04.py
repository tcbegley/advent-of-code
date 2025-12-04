import sys
from itertools import product


def load_data(path):
    with open(path) as f:
        return [list(row) for row in f.read().strip().split("\n")]


def get_neighbours(grid, r, c):
    n_rows = len(grid)
    n_cols = len(grid[0])

    for dr, dc in product((-1, 0, 1), (-1, 0, 1)):
        if dr == dc == 0 or not (
            0 <= (nr := r + dr) < n_rows and 0 <= (nc := c + dc) < n_cols
        ):
            continue
        yield (nr, nc)


def accessible_roll(grid, r, c):
    return (
        data[r][c] == "@"
        and sum(data[nr][nc] == "@" for nr, nc in get_neighbours(data, r, c)) < 4
    )


def part_1(data):
    return sum(
        accessible_roll(data, r, c)
        for r in range(len(data))
        for c in range(len(data[0]))
    )


def part_2(data):
    count = 0

    while True:
        count_iter = 0

        for r in range(len(data)):
            for c in range(len(data[0])):
                if accessible_roll(data, r, c):
                    data[r][c] = "."
                    count += 1
                    count_iter += 1

        if count_iter == 0:
            break

    return count


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
