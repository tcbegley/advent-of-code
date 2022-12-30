import sys
from itertools import product


def load_data(path):
    with open(path) as f:
        rows = f.read().strip().split("\n")

    m = {}
    for r, row in enumerate(rows):
        for c, char in enumerate(row):
            m[(r, c)] = char

    return m


def get_neighbours(loc):
    for (dr, dc) in product((-1, 0, 1), (-1, 0, 1)):
        if dr == 0 and dc == 0:
            continue
        yield (loc[0] + dr, loc[1] + dc)


def to_string(m):
    return "".join(m.values())


def simulate(m, n=10):
    seen = {}
    states = []

    for i in range(n):
        str_m = to_string(m)
        if str_m in seen:
            prev_i = seen[str_m]
            offset = (n - prev_i) % (i - prev_i)
            return states[prev_i + offset]

        seen[str_m] = i
        states.append(str_m)

        next_m = {}

        for loc, char in m.items():
            if char == ".":
                if sum(m.get(nbr) == "|" for nbr in get_neighbours(loc)) >= 3:
                    next_m[loc] = "|"
                else:
                    next_m[loc] = "."
            elif char == "|":
                if sum(m.get(nbr) == "#" for nbr in get_neighbours(loc)) >= 3:
                    next_m[loc] = "#"
                else:
                    next_m[loc] = "|"
            elif char == "#":
                if any(
                    m.get(nbr) == "#" for nbr in get_neighbours(loc)
                ) and any(m.get(nbr) == "|" for nbr in get_neighbours(loc)):
                    next_m[loc] = "#"
                else:
                    next_m[loc] = "."

        m = next_m

    return to_string(m)


def part_1(m):
    state = simulate(m)
    return sum(v == "|" for v in state) * sum(v == "#" for v in state)


def part_2(m):
    state = simulate(m, n=1_000_000_000)
    return sum(v == "|" for v in state) * sum(v == "#" for v in state)


if __name__ == "__main__":
    m = load_data(sys.argv[1])
    print(f"Part 1: {part_1(m)}")
    print(f"Part 2: {part_2(m)}")
