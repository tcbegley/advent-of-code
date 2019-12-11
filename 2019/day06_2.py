import sys
from collections import defaultdict


class Graph:
    def __init__(self):
        self.graph = defaultdict(set)

    def add_edge(self, u, v):
        self.graph[u].add(v)
        self.graph[v].add(u)

    def bfs(self, start):
        visited = defaultdict(lambda: -1)

        queue = [start]
        visited[start] = 0

        while queue:
            s = queue.pop(0)
            for i in self.graph[s]:
                if visited[i] == -1:
                    visited[i] = visited[s] + 1
                    queue.append(i)
        return visited["SAN"] - 2


def answer(path):
    with open(path) as f:
        edges = map(lambda x: x.split(")"), f.read().strip().split("\n"))

    g = Graph()
    for v1, v2 in edges:
        g.add_edge(v1, v2)

    return g.bfs("YOU")


if __name__ == "__main__":
    print(answer(sys.argv[1]))
