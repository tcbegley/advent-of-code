import sys
from collections import Counter, deque


def load_data(path):
    with open(path) as f:
        rows = f.read().strip().split("\n")

    grid = {}
    start, end = None, None

    for r, row in enumerate(rows):
        for c, char in enumerate(row):
            loc = (r, c)
            if char == "S":
                start = loc
                char = "."
            elif char == "E":
                end = loc
                char = "."
            grid[loc] = char

    return grid, start, end


def get_neighbours(loc, grid):
    for d in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if (nbr := (loc[0] + d[0], loc[1] + d[1])) in grid:
            yield nbr


def get_distances(grid, start, end):
    queue = deque([(0, end)])
    seen = {end}

    distances = {}

    while queue:
        dist, loc = queue.popleft()
        distances[loc] = dist

        for nbr in get_neighbours(loc, grid):
            if nbr not in seen and grid.get(nbr, "#") != "#":
                queue.append((dist + 1, nbr))
                seen.add(nbr)

    return distances


def get_cheats_from_loc(start, distances, grid, limit):
    queue = deque([(0, start)])
    seen = {start}

    while queue:
        steps, loc = queue.popleft()
        if steps > limit:
            break

        if (d1 := distances[start]) > (d2 := distances.get(loc, float("inf"))) + steps:
            yield d1 - d2 - steps

        for nbr in get_neighbours(loc, grid):
            if nbr not in seen:
                queue.append((steps + 1, nbr))
                seen.add(nbr)


def count_cheats(start, distances, grid, limit=2):
    cheats = Counter()
    queue = deque([start])
    seen = {start}

    while queue:
        loc = queue.popleft()
        cheats.update(get_cheats_from_loc(loc, distances, grid, limit))

        for nbr in get_neighbours(loc, grid):
            if nbr not in seen and grid[nbr] != "#":
                queue.append(nbr)
                seen.add(nbr)

    return sum(v for k, v in cheats.items() if k >= 100)


if __name__ == "__main__":
    grid, start, end = load_data(sys.argv[1])
    distances = get_distances(grid, start, end)
    print(f"Part 1: {count_cheats(start, distances, grid)}")
    print(f"Part 2: {count_cheats(start, distances, grid, limit=20)}")
