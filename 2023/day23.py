import sys
from collections import defaultdict

SLOPE_DIR = {"^": 1j, ">": 1, "v": -1j, "<": -1}


class Graph:
    def __init__(self):
        self.vertices = set()
        self.edges = defaultdict(list)

    def add_edge(self, src, dest, weight):
        self.vertices.update({src, dest})
        self.edges[src].append((dest, weight))


def load_data(path):
    with open(path) as f:
        return {
            c - r * 1j: char
            for r, row in enumerate(f.read().strip().split("\n"))
            for c, char in enumerate(row)
        }


def get_neighbours(loc, grid):
    if grid[loc] in SLOPE_DIR:
        yield loc + SLOPE_DIR[grid[loc]]
    else:
        for d in (1, -1, -1j, 1j):
            nbr = loc + d
            if (nbr_tile := grid.get(nbr, "#")) == "." or SLOPE_DIR.get(nbr_tile) == d:
                yield nbr


def follow_path(loc, previous, grid):
    # a lot of the route is single steps where there is no option. we condense these
    # into edges of a graph
    path = [loc]
    while (
        len(nbrs := [nbr for nbr in get_neighbours(loc, grid) if nbr != previous]) == 1
    ):
        loc, previous = nbrs[0], loc
        path.append(loc)
    return path


def build_graph(grid):
    start = max(
        (k for k in grid if k.imag == 0 and grid[k] == "."), key=lambda x: x.real
    )
    last_row = min(k.imag for k in grid)
    target = max(
        (k for k in grid if k.imag == last_row and grid[k] == "."), key=lambda x: x.real
    )

    vertices = {start, target}
    for loc, tile in grid.items():
        if (
            tile == "."
            and sum(grid.get(loc + d, "#") != "#" for d in (1, -1, 1j, -1j)) > 2
            and sum(
                SLOPE_DIR.get(nbr_tile, d) == d
                for d in (1, -1, 1j, -1j)
                if (nbr_tile := grid.get(loc + d, "#")) != "#"
            )
            > 1
        ):
            vertices.add(loc)

    g = Graph()
    for loc in vertices:
        for nbr in get_neighbours(loc, grid):
            path = follow_path(nbr, loc, grid)
            if path[-1] in vertices:
                g.add_edge(loc, path[-1], len(path))

    return g, start, target


def longest_traversal(graph, start, target):
    visited = {v: False for v in graph.vertices}
    visited[start] = True

    def backtrack(v, total_steps=0):
        if v == target:
            yield total_steps
        else:
            for nbr, steps in graph.edges[v]:
                if not visited[nbr]:
                    visited[nbr] = True
                    yield from backtrack(nbr, total_steps + steps)
                    visited[nbr] = False

    return max(backtrack(start))


def part_1(grid):
    graph, start, target = build_graph(grid)
    return longest_traversal(graph, start, target)


def part_2(grid):
    graph, start, target = build_graph(
        {k: v if v == "#" else "." for k, v in grid.items()}
    )
    return longest_traversal(graph, start, target)


if __name__ == "__main__":
    grid = load_data(sys.argv[1])
    print(f"Part 1: {part_1(grid)}")
    print(f"Part 2: {part_2(grid)}")
