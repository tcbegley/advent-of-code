import sys
from collections import deque
from string import ascii_lowercase

HEIGHT_MAP = {
    "S": 1,
    "E": 26,
    **{char: height for height, char in enumerate(ascii_lowercase, start=1)},
}


def load_data(path):
    with open(path) as f:
        data = list(f.read().strip().split("\n"))

    grid, start, end = {}, None, None
    for r, row in enumerate(data):
        for c, char in enumerate(row):
            grid[(r, c)] = HEIGHT_MAP[char]
            if char == "S":
                start = (r, c)
            elif char == "E":
                end = (r, c)

    return grid, start, end


def get_neighbours(loc, grid):
    r, c = loc
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        new_loc = (r + dr, c + dc)
        if new_loc in grid and grid[new_loc] <= grid[loc] + 1:
            yield new_loc


def bfs(grid, starts, end):
    queue = deque([(0, start) for start in starts])
    visited = set(starts)

    while queue:
        steps, loc = queue.popleft()
        if loc == end:
            return steps

        for nbr in get_neighbours(loc, grid):
            if nbr not in visited:
                visited.add(nbr)
                queue.append((steps + 1, nbr))

    raise RuntimeError("No solution found")


def part_1(grid, start, end):
    return bfs(grid, [start], end)


def part_2(grid, end):
    starts = [loc for loc, height in grid.items() if height == 1]
    return bfs(grid, starts, end)


if __name__ == "__main__":
    grid, start, end = load_data(sys.argv[1])
    print(f"Part 1: {part_1(grid, start, end)}")
    print(f"Part 2: {part_2(grid, end)}")
