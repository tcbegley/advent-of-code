import sys
from collections import defaultdict


class Graph:
    def __init__(self):
        self.graph = defaultdict(dict)

    def add_edge(self, u, v, weight):
        self.graph[u][v] = weight
        self.graph[v][u] = weight

    def travelling_salesman(self, op=min):
        # find optimal traversal by considering all start / end pairs
        nodes = set(self.graph)
        return op(
            [
                self._ts({n for n in nodes if n != start}, start, end, op)
                for start in nodes
                for end in {n for n in nodes if n != start}
            ]
        )

    def _ts(self, nodes, start, end, op=min):
        # recursively find optimal route start -> end via all nodes in nodes
        if nodes == {end}:
            return self.graph[start][end]

        new_nodes = nodes.copy()
        new_nodes.remove(end)

        dists = [
            self._ts(new_nodes, start, x, op) + self.graph[x][end]
            for x in nodes
            if end in self.graph[x]
        ]
        return op(dists)


def load_data(path):
    with open(path) as f:
        return [
            ((x := line.split(" "))[0], x[2], int(x[4]))
            for line in f.read().strip().split("\n")
        ]


def get_distance(distances, op=min):
    g = Graph()
    for start, end, distance in distances:
        g.add_edge(start, end, distance)

    return g.travelling_salesman(op)


def part_1(distances):
    return get_distance(distances)


def part_2(distances):
    return get_distance(distances, max)


if __name__ == "__main__":
    distances = load_data(sys.argv[1])
    print(f"Part 1: {part_1(distances)}")
    print(f"Part 2: {part_2(distances)}")
