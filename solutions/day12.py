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
        return len(visited.keys())


def answer(file_path):
    with open(file_path, 'r') as f:
        tmp = [x.split(' <-> ') for x in f.readlines()]
        edges = [(int(x[0]), list(map(int, x[1].split(', ')))) for x in tmp]
    g = Graph()
    for edge in edges:
        for v in edge[1]:
            g.add_edge(edge[0], v)
    return g.bfs(0)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
