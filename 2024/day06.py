import sys


def load_data(path):
    with open(path) as f:
        data = f.read().strip().split("\n")

    start = None
    grid = {}
    for r, row in enumerate(data):
        for c, char in enumerate(row):
            grid[c - r * 1j] = char
            if char == "^":
                start = c - r * 1j

    return grid, start


def will_loop(grid, loc, d, seen):
    # check if path starting at loc in direction d will end up in a loop
    while True:
        next_loc = loc + d
        match grid.get(next_loc):
            case "." | "^":
                if (next_loc, d) in seen:
                    return True
                loc = next_loc
                seen.add((next_loc, d))
            case "#":
                d *= -1j  # rotate right
            case None:
                return False


def simulate(grid, start):
    d = 1j  # initial direction is up
    loc = start
    seen = {(start, d)}

    count = 0
    while True:
        next_loc = loc + d
        match grid.get(next_loc):
            case "." | "^" as char:
                if char == "." and not any(
                    (next_loc, d_) in seen for d_ in (-1, 1, 1j, -1j)
                ):
                    # space in front of us could have a new obstacle placed in it, so
                    # we place it, and check if continuing to follow that path would
                    # result in a loop. if so, increment the count
                    grid[next_loc] = "#"
                    count += will_loop(grid, loc, d * -1j, {*seen})
                    grid[next_loc] = "."
                loc = next_loc
                seen.add((next_loc, d))
            case "#":
                d *= -1j  # rotate right
            case None:
                break

    return len({loc for loc, _ in seen}), count


if __name__ == "__main__":
    grid, start = load_data(sys.argv[1])
    part_1, part_2 = simulate(grid, start)
    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")
