import sys
from collections import defaultdict


class Graph:
    def __init__(self):
        self.graph = defaultdict(set)

    def add_edge(self, u, v):
        self.graph[u].add(v)
        self.graph[v].add(u)

    def bfs(self, start):
        visited = set()

        queue = [start]
        visited.add(start)

        while queue:
            s = queue.pop(0)
            for i in self.graph[s]:
                if i not in visited:
                    visited.add(i)
                    queue.append(i)

        return visited


def load_data(path):
    with open(path) as f:
        return [process_line(line) for line in f.readlines()]


def process_line(line):
    root, nbrs = line.split(" <-> ")
    return int(root), [int(nbr) for nbr in nbrs.split(", ")]


def build_graph(edges):
    g = Graph()
    for u, vs in edges:
        for v in vs:
            g.add_edge(u, v)
    return g


def part_1(edges):
    g = build_graph(edges)
    return len(g.bfs(0))


def part_2(edges):
    g = build_graph(edges)
    to_visit = {edge[0] for edge in edges}
    count = 0
    while to_visit:
        start = to_visit.pop()
        to_visit = to_visit - g.bfs(start)
        count += 1
    return count


if __name__ == "__main__":
    edges = load_data(sys.argv[1])
    print(f"Part 1: {part_1(edges)}")
    print(f"Part 2: {part_2(edges)}")
