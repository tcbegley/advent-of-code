import re
import sys
from collections import defaultdict

COLOR_PATTERN = re.compile(r"^\d+ (.*) bags?$")


class Graph:
    def __init__(self):
        self.graph = defaultdict(set)

    def add_edge(self, u, v):
        self.graph[u].add(v)

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


def extract_colors(s):
    s = s.rstrip(".")
    if s == "no other bags":
        return []

    s = s.split(", ")
    s = [COLOR_PATTERN.match(x) for x in s]
    return [m.group(1) for m in s if m]


def answer(path):
    with open(path) as f:
        rules = [
            r.split(" bags contain ") for r in f.read().strip().split("\n")
        ]

    rules = [(r, extract_colors(s)) for r, s in rules]

    g = Graph()

    for end, start_list in rules:
        for start in start_list:
            g.add_edge(start, end)

    return g.bfs("shiny gold") - 1  # don't count shiny gold bag


if __name__ == "__main__":
    print(answer(sys.argv[1]))
