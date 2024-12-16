import sys
from heapq import heappop, heappush


def load_data(path):
    with open(path) as f:
        raw_grid = f.read().strip()

    grid = {}
    start = end = None
    for r, row in enumerate(raw_grid.split("\n")):
        for c, char in enumerate(row):
            if char == "S":
                start = (c, -r)
            elif char == "E":
                end = (c, -r)
            grid[(c, -r)] = char

    return start, end, grid


def solve(start, end, grid):
    # start facing east
    queue = [(0, (1, 0), start, [start])]
    seen = {(start, (1, 0)): 0}

    best_score = float("inf")
    visited = set()

    while queue:
        score, current_dir, loc, locs = heappop(queue)

        if score > best_score:
            # found all of the best paths
            return best_score, len(visited)

        if loc == end:
            if score < best_score:
                best_score = score
            visited.update(locs)

        for d in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if (
                seen.get(
                    ((next_loc := (loc[0] + d[0], loc[1] + d[1])), d), float("inf")
                )
                >= score
                and grid[next_loc] != "#"
            ):
                next_score = score + 1 + 1000 * (d != current_dir)
                heappush(queue, (next_score, d, next_loc, [*locs, next_loc]))
                seen[(next_loc, d)] = next_score


if __name__ == "__main__":
    start, end, grid = load_data(sys.argv[1])
    score, n_visited = solve(start, end, grid)
    print(f"Part 1: {score}")
    print(f"Part 2: {n_visited}")
