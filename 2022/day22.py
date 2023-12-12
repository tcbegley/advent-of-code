import re
import sys
from itertools import chain, zip_longest

DIRS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
R_TURN = {"U": "R", "R": "D", "D": "L", "L": "U"}
L_TURN = {"U": "L", "L": "D", "D": "R", "R": "U"}
FACING = {"R": 0, "D": 1, "L": 2, "U": 3}


def load_data(path):
    with open(path) as f:
        map_, directions = f.read().split("\n\n")
    map_ = {
        (r, c): char
        for r, row in enumerate(map_.split("\n"), start=1)
        for c, char in enumerate(row, start=1)
        if char != " "
    }
    return map_, parse_directions(directions.strip())


def parse_directions(directions):
    pat = re.compile(r"R|L")
    return list(
        filter(
            lambda x: x is not None,
            chain.from_iterable(
                zip_longest(map(int, pat.split(directions)), pat.findall(directions))
            ),
        )
    )


def add(loc1, loc2):
    (r1, c1), (r2, c2) = loc1, loc2
    return (r1 + r2, c1 + c2)


def wrap2(_, next_loc):
    # this is specific to my input. I haven't had the motivation to figure out
    # a general approach to cube wrapping...
    r, c = next_loc
    if r == 0:
        if 51 <= c <= 100:
            return (c + 100, 1), "R"
        elif 101 <= c <= 150:
            return (200, c - 100), "U"
    elif c == 151:
        if 1 <= r <= 50:
            return (151 - r, 100), "L"
    elif r == 51:
        if 101 <= c <= 150:
            return (c - 50, 100), "L"
    elif c == 101:
        if 51 <= r <= 100:
            return (50, r + 50), "U"
        elif 101 <= r <= 150:
            return (151 - r, 150), "L"
    if r == 151:
        if 51 <= c <= 100:
            return (c + 100, 50), "L"
    if c == 51:
        if 151 <= r <= 200:
            return (150, r - 100), "U"
    if r == 201:
        if 1 <= c <= 50:
            return (1, c + 100), "D"
    if c == 0:
        if 151 <= r <= 200:
            return (1, r - 100), "D"
        elif 101 <= r <= 150:
            return (151 - r, 51), "R"
    if r == 100:
        if 1 <= c <= 50:
            return (c + 50, 51), "R"
    if c == 50:
        if 51 <= r <= 100:
            return (101, r - 50), "D"
        elif 1 <= r <= 50:
            return (151 - r, 1), "R"


def walk(map_, directions, wrap_fn):
    loc, d = (1, min(c for r, c in map_ if r == 1)), "R"

    for direction in directions:
        if direction == "R":
            d = R_TURN[d]
        elif direction == "L":
            d = L_TURN[d]
        else:
            while direction > 0:
                next_loc = add(loc, DIRS[d])
                next_d = d
                if next_loc not in map_:
                    next_loc, next_d = wrap_fn(d, next_loc)
                if map_[next_loc] == "#":
                    break
                loc, d = next_loc, next_d
                direction -= 1

    return 1000 * loc[0] + 4 * loc[1] + FACING[d]


def part_1(map_, directions):
    n_rows = max(r for r, _ in map_)
    n_cols = max(c for _, c in map_)
    rows = {
        row: (
            min(c for r, c in map_ if r == row),
            max(c for r, c in map_ if r == row),
        )
        for row in range(1, n_rows + 1)
    }
    cols = {
        col: (
            min(r for r, c in map_ if c == col),
            max(r for r, c in map_ if c == col),
        )
        for col in range(1, n_cols + 1)
    }

    def wrap(d, next_loc):
        if d == "U":
            return (cols[next_loc[1]][1], next_loc[1]), "U"
        elif d == "R":
            return (next_loc[0], rows[next_loc[0]][0]), "R"
        elif d == "D":
            return (cols[next_loc[1]][0], next_loc[1]), "D"
        elif d == "L":
            return (next_loc[0], rows[next_loc[0]][1]), "L"

    return walk(map_, directions, wrap)


def part_2(map_, directions):
    return walk(map_, directions, wrap2)


if __name__ == "__main__":
    map_, directions = load_data(sys.argv[1])
    print(f"Part 1: {part_1(map_, directions)}")
    print(f"Part 2: {part_2(map_, directions)}")
