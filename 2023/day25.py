import sys
from collections import defaultdict, deque
from itertools import combinations


class Graph:
    def __init__(self):
        self.vertices = set()
        self.edges = defaultdict(set)

    def add_edge(self, source, target):
        self.vertices.update({source, target})
        self.edges[source].add(target)
        self.edges[target].add(source)


def load_graph(path):
    with open(path) as f:
        rows = f.read().strip().split("\n")

    graph = Graph()
    for row in rows:
        source, targets = row.split(": ")
        for target in targets.split(" "):
            graph.add_edge(source, target)

    return graph


def max_flow(graph, source, target):
    edge_connectivity = 0
    used_edges = set()

    while True:
        queue = deque([source])
        visited = {source: None}

        while queue:
            node = queue.popleft()
            if node == target:
                break
            for nbr in graph.edges[node]:
                # if an edge has been used in one direction it can't be used in the
                # other, so we identify them via a sorted tuple of end points
                edge = tuple(sorted([node, nbr]))
                if edge not in used_edges and nbr not in visited:
                    visited[nbr] = node
                    queue.append(nbr)
        else:
            # no path found
            break

        node = target
        while node != source:
            edge = tuple(sorted([node, visited[node]]))
            used_edges.add(edge)
            node = visited[node]

        edge_connectivity += 1

    return used_edges, edge_connectivity


def min_cut(graph, source, used_edges):
    queue = deque([source])
    reachable = {source}

    while queue:
        node = queue.popleft()
        for nbr in graph.edges[node]:
            edge = tuple(sorted([node, nbr]))
            if edge not in used_edges and nbr not in reachable:
                reachable.add(nbr)
                queue.append(nbr)

    return reachable


def part_1(graph):
    # find two nodes that have edge connectivity 3, get the min cut and find the nodes
    # in one of the pieces. this gets us the answer
    for source, target in combinations(graph.vertices, 2):
        used_edges, edge_connectivity = max_flow(graph, source, target)
        if edge_connectivity == 3:
            n = len(min_cut(graph, source, used_edges))
            return n * (len(graph.vertices) - n)


if __name__ == "__main__":
    graph = load_graph(sys.argv[1])
    print(f"Part 1: {part_1(graph)}")
