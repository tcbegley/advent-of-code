import heapq
import itertools
import sys
from collections import namedtuple

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))
VALID_DIRECTIONS = {
    (1, 0): ((1, 0), (0, -1), (0, 1)),
    (-1, 0): ((-1, 0), (0, 1), (0, -1)),
    (0, 1): ((0, 1), (-1, 0), (1, 0)),
    (0, -1): ((0, -1), (-1, 0), (1, 0)),
    (0, 0): DIRECTIONS,
}

# we will do a graph search to solve this problem. Each "node" in the graph corresponds
# to a location in the grid, as well as the incoming direction and the number of steps
# in that direction that have been taken so far.
Node = namedtuple("Node", ["loc", "direction", "count"])


def load_data(path):
    with open(path) as f:
        return {
            (r, c): int(char)  # convert rows / columns to x / y directions
            for r, row in enumerate(f.read().strip().split("\n"))
            for c, char in enumerate(row)
        }


def add(loc1, loc2):
    return (loc1[0] + loc2[0], loc1[1] + loc2[1])


def make_get_neighbours(grid, min_steps, max_steps, n_rows, n_cols):
    def get_neighbours(node):
        for direction in VALID_DIRECTIONS[node.direction]:
            if direction != node.direction:
                new_loc = node.loc
                cost = 0
                for _ in range(min_steps):
                    new_loc = add(new_loc, direction)
                    cost += grid.get(new_loc, 0)
                nbr = Node(loc=new_loc, direction=direction, count=min_steps)
                if 0 <= new_loc[0] < n_rows and 0 <= new_loc[1] < n_cols:
                    yield nbr, cost
            elif node.count < max_steps:
                new_loc = add(node.loc, direction)
                cost = grid.get(new_loc, 0)
                nbr = Node(new_loc, direction, node.count + 1)
                if 0 <= new_loc[0] < n_rows and 0 <= new_loc[1] < n_cols:
                    yield nbr, cost

    return get_neighbours


def shortest_path(grid, min_steps=1, max_steps=3):
    dist = {
        Node(*args): float("inf")
        for args in itertools.product(grid, DIRECTIONS, range(min_steps, max_steps + 1))
    }

    start = Node(loc=(0, 0), direction=(0, 0), count=0)
    dist[start] = 0

    n_rows = max(r for r, _ in grid) + 1
    n_cols = max(c for _, c in grid) + 1
    target_loc = (n_cols - 1, n_rows - 1)
    finalised = set()
    queue = []
    heapq.heappush(queue, (0, start))

    get_neighbours = make_get_neighbours(
        grid, min_steps, max_steps, n_rows=n_rows, n_cols=n_cols
    )

    while queue:
        if (
            min_distance := min(
                (
                    dist[Node(target_loc, direction, count)]
                    for direction, count in itertools.product(
                        DIRECTIONS, range(min_steps, max_steps + 1)
                    )
                    if Node(target_loc, direction, count) in finalised
                ),
                default=float("inf"),
            )
        ) < float("inf"):
            return min_distance

        min_cost_to_loc, node = heapq.heappop(queue)
        finalised.add(node)

        for nbr, cost in get_neighbours(node):
            if nbr not in finalised:
                old_dist = dist[nbr]
                new_dist = dist[node] + cost
                if new_dist < old_dist:
                    dist[nbr] = min_cost_to_loc + cost
                    heapq.heappush(queue, (dist[nbr], nbr))

    raise ValueError("No path found...")


def part_1(data):
    return shortest_path(data)


def part_2(data):
    return shortest_path(data, min_steps=4, max_steps=10)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
