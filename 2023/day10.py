import sys

DIRECTION_LOOKUP = {
    "|": {(0, 2): (0, 2), (0, -2): (0, -2)},
    "-": {(2, 0): (2, 0), (-2, 0): (-2, 0)},
    "L": {(0, -2): (2, 0), (-2, 0): (0, 2)},
    "J": {(0, -2): (-2, 0), (2, 0): (0, 2)},
    "7": {(2, 0): (0, -2), (0, 2): (-2, 0)},
    "F": {(0, 2): (2, 0), (-2, 0): (0, -2)},
    ".": {},
    "S": {d: d for d in ((2, 0), (-2, 0), (0, 2), (0, -2))},
}


def load_data(path):
    with open(path) as f:
        return {
            (2 * c, -2 * r): char  # convert rows / columns to x / y directions
            for r, row in enumerate(f.read().strip().split("\n"))
            for c, char in enumerate(row)
        }


def next_loc(loc, d):
    return (loc[0] + d[0], loc[1] + d[1]), (
        loc[0] + d[0] // 2,
        loc[1] + d[1] // 2,
    )


def get_distances(data):
    for start_loc, v in data.items():
        if v == "S":
            break

    for direction in ((2, 0), (-2, 0), (0, 2), (0, -2)):
        if (
            direction
            in DIRECTION_LOOKUP[data[next_loc(start_loc, direction)[0]]]
        ):
            break

    loc = start_loc
    count = 0
    distances = {}

    while loc != start_loc or count == 0:
        loc, intermediate = next_loc(loc, direction)
        count += 1
        distances[loc] = distances[intermediate] = count
        direction = DIRECTION_LOOKUP[data[loc]][direction]

    distances = {k: min(v, count - v) for k, v in distances.items()}
    print(distances[(0, 2)], distances[(0, -2)])


def part_1(data):
    distances = get_distances(data)
    return max(distances.values())


def part_2(data):
    distances = get_distances(data)
    minx, maxx = min(x for x, _ in distances), max(x for x, _ in distances)
    miny, maxy = min(y for _, y in distances), max(y for _, y in distances)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
