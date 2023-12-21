import sys
from collections import deque


def load_data(path):
    with open(path) as f:
        grid = {
            (r, c): char
            for r, row in enumerate(f.read().strip().split("\n"))
            for c, char in enumerate(row)
        }

    for k, v in grid.items():
        if v == "S":
            start = k
            grid[k] = "."
    return grid, start


def make_get_neighbours(grid):
    nrows = max(r for r, _ in grid) + 1
    ncols = max(c for _, c in grid) + 1
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))

    def get_neighbours(loc):
        for d in dirs:
            nbr = (loc[0] + d[0], loc[1] + d[1])
            if grid.get((nbr[0] % nrows, nbr[1] % ncols), "#") != "#":
                yield nbr

    return get_neighbours


def bfs(grid, start, n):
    queue = deque([(start, 0)])
    count = 0
    seen = {start}
    get_neighbours = make_get_neighbours(grid)
    n_mod_2 = n % 2

    while queue:
        loc, steps = queue.popleft()
        if steps % 2 == n_mod_2:
            count += 1

        if steps < n:
            for nbr in get_neighbours(loc):
                if nbr not in seen:
                    seen.add(nbr)
                    queue.append((nbr, steps + 1))

    return count


def part_1(grid, start):
    return bfs(grid, start, n=64)


def part_2(grid, start):
    # we can reach the start points of the four neighbouring tiles every 131 steps
    # the number of new start points grows linearly (4, 8, 12, ...)
    # so the number of tiles in play grows quadratically
    # therefore we can say count(65), count(65 + 131), count(65 + 2 * 131) is a
    # quadratic polynomial.
    # since 26501365 = 65 + 202300 * 131, we just need to evaluate this polynomial at
    # 202300 to get the final answer
    # we do so by evaluating the first three points, then extrapolating using the
    # differences (differences grow by a constant factor)
    p0, p1, p2 = [bfs(grid, start, n=65 + i * 131) for i in range(3)]

    diff = (p2 - p1) - (p1 - p0)
    n = 202_300
    return p2 + (n - 2) * (p2 - p1) + (n - 2) * (n - 1) // 2 * diff


if __name__ == "__main__":
    grid, start = load_data(sys.argv[1])
    print(f"Part 1: {part_1(grid, start)}")
    print(f"Part 2: {part_2(grid, start)}")
