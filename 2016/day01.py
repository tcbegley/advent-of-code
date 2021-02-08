import sys

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def load_data(path):
    with open(path) as f:
        return f.read().strip().split(", ")


def l1(x):
    return sum(map(abs, x))


def follow_directions(directions):
    loc, d = (0, 0), 0
    yield loc

    for direction in directions:
        turn, steps = direction[0], int(direction[1:])
        if turn == "R":
            d = (d + 1) % 4
        else:
            d = (d - 1) % 4

        for _ in range(steps):
            loc = tuple(x + dx for x, dx in zip(loc, DIRS[d]))
            yield loc


def part_1(directions):
    locs = list(follow_directions(directions))
    return l1(locs[-1])


def part_2(directions):
    locs = follow_directions(directions)
    seen = set()
    for loc in locs:
        if loc in seen:
            break
        seen.add(loc)
    return l1(loc)


if __name__ == "__main__":
    directions = load_data(sys.argv[1])
    print(f"Part 1: {part_1(directions)}")
    print(f"Part 2: {part_2(directions)}")
