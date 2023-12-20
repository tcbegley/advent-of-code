import sys
from collections import deque

DIRECTION_LOOKUP = {
    "U": 1j,
    "R": 1,
    "D": -1j,
    "L": -1,
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U",
}


def process_row(row):
    direction, steps, colour = row.split(" ")
    steps = int(steps)
    colour = colour.removeprefix("(#").removesuffix(")")
    return (direction, steps, colour)


def load_data(path):
    with open(path) as f:
        rows = f.read().strip().split("\n")

    return [process_row(row) for row in rows]


def format_grid(grid):
    x_min, x_max = int(min(k.real for k in grid)), int(max(k.real for k in grid))
    y_min, y_max = int(min(k.imag for k in grid)), int(max(k.imag for k in grid))

    return "\n".join(
        "".join(grid.get(x + y * 1j, "-") for x in range(x_min, x_max + 1))
        for y in range(y_max, y_min - 1, -1)
    )


def tunnel(data, part_2=False):
    loc = 0
    grid = {}
    for direction, steps, code in data:
        if part_2:
            d = DIRECTION_LOOKUP[code[-1]]
            steps = int(code[:-1], base=16)
        else:
            d = DIRECTION_LOOKUP[direction]
        for _ in range(steps):
            loc += d
            grid[loc] = "#"
    return grid


def fill_exterior(grid):
    x_min, x_max = int(min(k.real for k in grid)), int(max(k.real for k in grid))
    y_min, y_max = int(min(k.imag for k in grid)), int(max(k.imag for k in grid))

    start = (x_min - 1) + (y_min - 1) * 1j
    queue = deque([start])
    grid[start] = "."

    while queue:
        loc = queue.popleft()
        grid[loc] = "."

        for d in (1, -1, 1j, -1j):
            nbr = loc + d
            if (
                x_min - 1 <= nbr.real <= x_max + 1
                and y_min - 1 <= nbr.imag <= y_max + 1
                and nbr not in grid
            ):
                grid[nbr] = "."
                queue.append(nbr)

    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            if (loc := x + y * 1j) not in grid:
                grid[loc] = "#"

    return grid


def part_1(data):
    return sum(v == "#" for v in fill_exterior(tunnel(data)).values())


def part_2(data):
    for _, _, code in data:
        print(f"{DIRECTION_LOOKUP[code[-1]]} {int(code[:-1], 16)}")


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
