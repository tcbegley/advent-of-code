import heapq
import sys
from itertools import product


def load_data(path):
    with open(path) as f:
        return {
            (i, j): int(value)
            for i, line in enumerate(f.readlines())
            for j, value in enumerate(line.strip())
        }


def get_neighbours(loc, n_rows, n_cols):
    neighbours = []
    x, y = loc
    for i in [-1, 1]:
        if 0 <= x + i < n_rows:
            neighbours.append((x + i, y))
        if 0 <= y + i < n_cols:
            neighbours.append((x, y + i))
    return neighbours


def answer(cost):
    n_rows = max(i for i, _ in cost) + 1
    n_cols = max(j for _, j in cost) + 1
    target = (n_rows - 1, n_cols - 1)
    finalised = set()

    queue = []
    heapq.heappush(queue, (0, (0, 0)))

    dist = {loc: float("inf") for loc in product(range(n_rows), range(n_cols))}
    dist[(0, 0)] = 0

    while len(finalised) < len(cost):
        if target in finalised:
            return dist[target]

        min_cost_to_loc, loc = heapq.heappop(queue)
        finalised.add(loc)

        for nbr in get_neighbours(loc, n_rows, n_cols):
            if nbr not in finalised:
                old_dist = dist[nbr]
                new_dist = dist[loc] + cost[nbr]
                if new_dist < old_dist:
                    dist[nbr] = min_cost_to_loc + cost[nbr]
                    heapq.heappush(queue, (dist[nbr], nbr))

    return dist[target]


def extend(cost):
    n_rows = max(i for i, _ in cost) + 1
    n_cols = max(j for _, j in cost) + 1
    new_cost = {}
    for i in range(5):
        for j in range(5):
            for loc in cost:
                new_cost[(n_rows * i + loc[0], n_cols * j + loc[1])] = (
                    cost[loc] + i + j - 1
                ) % 9 + 1
    return new_cost


def part_1(cost):
    return answer(cost)


def part_2(cost):
    cost = extend(cost)
    return answer(cost)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
