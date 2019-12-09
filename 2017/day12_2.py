import sys
from collections import defaultdict


class Graph:
    def __init__(self):
        self.graph = defaultdict(set)

    def add_edge(self, u, v):
        self.graph[u].add(v)
        self.graph[v].add(u)

    def bfs(self, start):
        visited = defaultdict(lambda: False)

        queue = [start]
        visited[start] = True

        while queue:
            s = queue.pop(0)
            for i in self.graph[s]:
                if not visited[i]:
                    visited[i] = True
                    queue.append(i)
        return set(visited.keys())


def answer(file_path):
    with open(file_path, "r") as f:
        tmp = [x.split(" <-> ") for x in f.readlines()]
        edges = [(int(x[0]), list(map(int, x[1].split(", ")))) for x in tmp]
    g = Graph()
    to_visit = set(edge[0] for edge in edges)
    for edge in edges:
        for v in edge[1]:
            g.add_edge(edge[0], v)
    count = 0
    while to_visit:
        start = to_visit.pop()
        to_visit = to_visit - g.bfs(start)
        count += 1
    return count


if __name__ == "__main__":
    print(answer(sys.argv[1]))
