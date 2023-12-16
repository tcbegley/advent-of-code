import sys
from collections import deque

DIRECTION_LOOKUP = {
    "/": {1: [1j], -1: [-1j], -1j: [-1], 1j: [1]},
    "\\": {1: [-1j], -1: [1j], 1j: [-1], -1j: [1]},
    "-": {1: [1], -1: [-1], 1j: [1, -1], -1j: [1, -1]},
    "|": {1: [1j, -1j], -1: [1j, -1j], 1j: [1j], -1j: [-1j]},
    ".": {k: [k] for k in [1, -1, 1j, -1j]},
}


def load_data(path):
    with open(path) as f:
        return {
            c - r * 1j: char  # convert rows / columns to x / y directions
            for r, row in enumerate(f.read().strip().split("\n"))
            for c, char in enumerate(row)
        }


def count_energised(grid, start_loc=0, start_dir=1):
    visited = {(start_loc, start_dir)}
    queue = deque([(start_loc, start_dir)])  # start top left, moving right

    while queue:
        location, direction = queue.popleft()

        for d in DIRECTION_LOOKUP[grid[location]][direction]:
            new_loc = location + d
            if new_loc in grid and (new_loc, d) not in visited:
                queue.append((new_loc, d))
                visited.add((new_loc, d))

    return len(set(loc for loc, _ in visited))


def part_1(grid):
    return count_energised(grid)


def part_2(grid):
    n_rows = int(max(-k.imag for k in grid) + 1)
    n_cols = int(max(k.real for k in grid) + 1)

    return max(
        max(count_energised(grid, -row * 1j, 1) for row in range(n_rows)),
        max(count_energised(grid, n_cols - 1 - row * 1j, -1) for row in range(n_rows)),
        max(count_energised(grid, col, -1j) for col in range(n_cols)),
        max(
            count_energised(grid, col - (n_rows - 1) * 1j, 1j) for col in range(n_cols)
        ),
    )


if __name__ == "__main__":
    grid = load_data(sys.argv[1])
    print(f"Part 1: {part_1(grid)}")
    print(f"Part 2: {part_2(grid)}")
