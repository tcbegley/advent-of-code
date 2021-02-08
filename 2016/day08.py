import re
import sys
from collections import deque
from itertools import chain

NUMBER = re.compile(r"\d+")


def load_data(path):
    with open(path) as f:
        return [process_line(line) for line in f.readlines()]


def process_line(line):
    a, b = map(int, NUMBER.findall(line))
    if line.startswith("rect"):
        return ("rect", a, b)
    elif line.startswith("rotate row"):
        return ("row", a, b)
    elif line.startswith("rotate column"):
        return ("col", a, b)


def rect(w, h, screen):
    for i in range(h):
        for j in range(w):
            screen[i][j] = True


def rotate_row(x, y, screen):
    row = deque(screen[x])
    row.rotate(y)
    screen[x] = list(row)


def rotate_col(x, y, screen):
    col = deque(row[x] for row in screen)
    col.rotate(y)
    for i, val in enumerate(col):
        screen[i][x] = val


def to_string(screen):
    return "\n".join("".join("#" if c else "." for c in row) for row in screen)


def populate_screen(commands, cols=50, rows=6):
    screen = [[False] * cols for _ in range(rows)]
    for cmd, x, y in commands:
        if cmd == "rect":
            rect(x, y, screen)
        elif cmd == "row":
            rotate_row(x, y, screen)
        elif cmd == "col":
            rotate_col(x, y, screen)

    return screen


def part_1(commands):
    screen = populate_screen(commands)
    return sum(chain.from_iterable(screen))


def part_2(commands):
    screen = populate_screen(commands)
    return f"\n{to_string(screen)}"


if __name__ == "__main__":
    commands = load_data(sys.argv[1])
    print(f"Part 1: {part_1(commands)}")
    print(f"Part 2: {part_2(commands)}")
