import sys
from collections import deque

MOVE_LOOKUP = {"^": 1j, "v": -1j, ">": 1, "<": -1}
ROBOT = "@"
WALL = "#"
BOX = "O"
BOX_LEFT = "["
BOX_RIGHT = "]"
EMPTY = "."


def load_data(path):
    with open(path) as f:
        raw_grid, moves = f.read().strip().split("\n\n")

    grid = {}
    robot = None
    for r, row in enumerate(raw_grid.split("\n")):
        for c, char in enumerate(row):
            grid[c - r * 1j] = char
            if char == ROBOT:
                robot = c - r * 1j

    moves = moves.replace("\n", "")

    return grid, robot, moves


def print_grid(grid):
    n_rows = 1 + max(-int(k.imag) for k in grid)
    n_cols = 1 + max(int(k.real) for k in grid)

    print(
        "\n".join(
            "".join(grid[c - r * 1j] for c in range(n_cols)) for r in range(n_rows)
        )
    )


def expand_grid(grid):
    new_grid = {}
    for k, c in grid.items():
        if c in [WALL, EMPTY]:
            a = b = c
        elif c == BOX:
            a = BOX_LEFT
            b = BOX_RIGHT
        elif c == ROBOT:
            a = ROBOT
            b = "."
        new_grid[k + k.real] = a
        new_grid[k + k.real + 1] = b

    return new_grid


def solve(grid, robot, moves):
    for move in moves:
        d = MOVE_LOOKUP[move]

        moving = {robot: "@"}
        queue = deque([robot])

        while queue:
            item = queue.popleft()

            if item + 1 not in moving and grid[item] == BOX_LEFT:
                queue.append(item + 1)
                moving[item + 1] = grid[item + 1]
            elif item - 1 not in moving and grid[item] == BOX_RIGHT:
                queue.append(item - 1)
                moving[item - 1] = grid[item - 1]

            if item + d not in moving and grid.get(item + d) not in (EMPTY, WALL):
                queue.append(item + d)
                moving[item + d] = grid[item + d]

        if all(grid.get(loc + d) != WALL for loc in moving):
            for loc in moving:
                grid[loc] = "."

            for loc, char in moving.items():
                grid[loc + d] = char
            robot += d

    return sum(
        int(k.real) - 100 * int(k.imag) for k, v in grid.items() if v in [BOX, BOX_LEFT]
    )


def part_1(grid, robot, moves):
    return solve(grid, robot, moves)


def part_2(grid, robot, moves):
    return solve(grid, robot, moves)


if __name__ == "__main__":
    grid, robot, moves = load_data(sys.argv[1])
    expanded_grid = expand_grid(grid)
    print(f"Part 1: {part_1(grid, robot, moves)}")
    print(f"Part 2: {part_2(expanded_grid, robot + robot.real, moves)}")
