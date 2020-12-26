import re
import sys
from collections import defaultdict


class Graph:
    def __init__(self):
        self.graph = defaultdict(lambda: defaultdict(lambda: 0))

    def add_edge(self, u, v, weight):
        self.graph[u][v] += weight
        self.graph[v][u] += weight

    def travelling_salesman(self):
        nodes = set(self.graph)
        start = next(iter(nodes))
        new_nodes = {n for n in nodes if n != start}
        return max(
            [
                self._ts(new_nodes, start, end) + self.graph[end][start]
                for end in new_nodes
                if start in self.graph[end]
            ]
        )

    def _ts(self, nodes, start, end):
        # recursively find optimal route start -> end via all nodes in nodes
        if nodes == {end}:
            return self.graph[start][end]

        new_nodes = nodes.copy()
        new_nodes.remove(end)

        dists = [
            self._ts(new_nodes, start, x) + self.graph[x][end]
            for x in nodes
            if end in self.graph[x]
        ]
        return max(dists)


PATTERN = re.compile(
    r"(\w+) would (\w+) (\d+) happiness units by sitting next to (\w+)."
)


def load_data(path):
    with open(path) as f:
        return list(map(process_line, f.read().strip().split("\n")))


def process_line(line):
    g = PATTERN.fullmatch(line).group
    if g(2) == "gain":
        return (g(1), g(4), int(g(3)))
    if g(2) == "lose":
        return (g(1), g(4), -int(g(3)))


def find_optimal_score(edges):
    g = Graph()
    for u, v, w in edges:
        g.add_edge(u, v, w)

    return g.travelling_salesman()


def part_1(edges):
    return find_optimal_score(edges)


def part_2(edges):
    people = {e[0] for e in edges}
    edges.extend(("Me", p, 0) for p in people)
    return find_optimal_score(edges)


if __name__ == "__main__":
    edges = load_data(sys.argv[1])
    print(f"Part 1: {part_1(edges)}")
    print(f"Part 2: {part_2(edges)}")
