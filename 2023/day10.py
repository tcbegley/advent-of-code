import sys
from collections import deque

# we take two steps in every direction so that in part 2 we can squeeze through gaps
# by traversion odd numbered tiles
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


def add_locs(loc1, loc2):
    return (loc1[0] + loc2[0], loc1[1] + loc2[1])


def get_distances(data):
    for start_loc, v in data.items():
        if v == "S":
            break

    for direction in ((2, 0), (-2, 0), (0, 2), (0, -2)):
        if direction in DIRECTION_LOOKUP[data[add_locs(start_loc, direction)]]:
            break

    loc = start_loc
    count = 0
    distances = {}

    while loc != start_loc or count == 0:
        # keep track of intermediate locations that we traversed so that we can block
        # them out in the distance map
        intermediate = add_locs(loc, (direction[0] // 2, direction[1] // 2))
        loc = add_locs(loc, direction)
        count += 1
        distances[loc] = distances[intermediate] = count
        direction = DIRECTION_LOOKUP[data[loc]][direction]

    distances = {k: min(v, count - v) for k, v in distances.items()}
    return distances


def bfs(distances, start, xrange, yrange):
    # in part 2 we do a breadth-first search from outside the track to mark off any
    # tiles that are reachable from the outside.
    queue = deque([start])

    while queue:
        loc = queue.popleft()

        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nbr = add_locs(loc, d)
            if (
                (xrange[0] <= nbr[0] <= xrange[1])
                and (yrange[0] <= nbr[1] <= yrange[1])
                and nbr not in distances
            ):
                distances[nbr] = float("inf")
                queue.append(nbr)


def part_1(data):
    distances = get_distances(data)
    return max(distances.values())


def part_2(data):
    distances = get_distances(data)
    minx, maxx = (
        min(x for x, _ in distances) - 1,
        max(x for x, _ in distances) + 1,
    )
    miny, maxy = (
        min(y for _, y in distances) - 1,
        max(y for _, y in distances) + 1,
    )

    bfs(distances, (minx, miny), (minx, maxx), (miny, maxy))

    # when summing the tiles that we have not been able to visit, we must make sure
    # we sum only those for whom both coordinates are even numbers
    return sum(
        (x % 2 == 0) and (y % 2 == 0) and (x, y) not in distances
        for x in range(minx, maxx + 1)
        for y in range(miny, maxy + 1)
    )


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
