import heapq
import itertools
import sys

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))
VALID_DIRECTIONS = {
    (1, 0): ((1, 0), (0, -1), (0, 1)),
    (-1, 0): ((-1, 0), (0, 1), (0, -1)),
    (0, 1): ((0, 1), (-1, 0), (1, 0)),
    (0, -1): ((0, -1), (-1, 0), (1, 0)),
    (0, 0): DIRECTIONS,
}


def load_data(path):
    with open(path) as f:
        return {
            (r, c): int(char)  # convert rows / columns to x / y directions
            for r, row in enumerate(f.read().strip().split("\n"))
            for c, char in enumerate(row)
        }


def add(loc1, loc2):
    return (loc1[0] + loc2[0], loc1[1] + loc2[1])


def get_neighbours(loc, d, count, n_rows, n_cols, min_steps, max_steps):
    for direction in VALID_DIRECTIONS[d]:
        new_loc = add(loc, direction)
        if 0 <= new_loc[0] < n_rows and 0 <= new_loc[1] < n_cols:
            if direction != d and not (1 <= count < min_steps):
                yield (new_loc, direction, 1)
            elif count < max_steps:
                yield (new_loc, d, count + 1)


def shortest_path(grid, min_steps=1, max_steps=3):
    dist = {
        (loc, direction, count): float("inf")
        for loc, direction, count in itertools.product(
            grid, DIRECTIONS, range(1, max_steps + 1)
        )
    }
    # start point has no direction associated
    dist[((0, 0), (0, 0), 0)] = 0

    n_rows = max(r for r, _ in grid) + 1
    n_cols = max(c for _, c in grid) + 1
    target = (n_cols - 1, n_rows - 1)
    finalised = set()
    queue = []
    heapq.heappush(queue, (0, (0, 0), (0, 0), 0))

    while queue:
        if (
            min_distance := min(
                (
                    dist[(target, direction, count)]
                    for direction, count in itertools.product(
                        DIRECTIONS, range(1, max_steps + 1)
                    )
                    if (target, direction, count) in finalised and count >= min_steps
                ),
                default=float("inf"),
            )
        ) < float("inf"):
            return min_distance

        min_cost_to_loc, loc, d, count = heapq.heappop(queue)
        finalised.add((loc, d, count))

        for nbr, next_d, next_count in get_neighbours(
            loc,
            d,
            count,
            n_rows=n_rows,
            n_cols=n_cols,
            min_steps=min_steps,
            max_steps=max_steps,
        ):
            if nbr not in finalised:
                old_dist = dist[(nbr, next_d, next_count)]
                new_dist = dist[(loc, d, count)] + grid[nbr]
                if new_dist < old_dist:
                    dist[(nbr, next_d, next_count)] = min_cost_to_loc + grid[nbr]
                    heapq.heappush(
                        queue,
                        (dist[(nbr, next_d, next_count)], nbr, next_d, next_count),
                    )

    raise ValueError("No path found...")


def part_1(data):
    return shortest_path(data)


def part_2(data):
    return shortest_path(data, min_steps=4, max_steps=10)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
