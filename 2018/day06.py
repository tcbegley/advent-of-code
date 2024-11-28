import sys
from collections import Counter


def load_data(path):
    with open(path) as f:
        return [tuple(map(int, row.split(","))) for row in f.read().strip().split("\n")]


def compute_grid(coords):
    xs, ys = zip(*coords)
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    # compute manhattan distance to centers for each point in the grid
    grid = {
        (x, y): [abs(x - cx) + abs(y - cy) for cx, cy in coords]
        for x in range(min_x, max_x + 1)
        for y in range(min_y, max_y)
    }

    return grid, (min_x, max_x), (min_y, max_y)


def part_1(coords):
    grid, (min_x, max_x), (min_y, max_y) = compute_grid(coords)

    counts = Counter()
    disqualified = set()

    for coord, dists in grid.items():
        min_dist = min(dists)
        if dists.count(min_dist) == 1:
            # increment count if exactly one group acheives the min distance
            counts[(group := dists.index(min_dist))] += 1
            if coord[0] in (min_x, max_x) or coord[1] in (min_y, max_y):
                # disqualify group if they claim a boundary point (in this
                # case that group will claim infinitely many points)
                disqualified.add(group)

    for group in disqualified:
        del counts[group]

    return counts.most_common(1)[0][1]


def part_2(coords):
    grid, *_ = compute_grid(coords)

    count = 0
    for dists in grid.values():
        if sum(dists) < 10_000:
            count += 1

    return count


if __name__ == "__main__":
    coords = load_data(sys.argv[1])
    print(f"Part 1: {part_1(coords)}")
    print(f"Part 2: {part_2(coords)}")
