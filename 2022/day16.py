import re
import sys
from collections import defaultdict
from functools import cache


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = defaultdict(set)
        self.distances = {}

    def add_node(self, node, value):
        self.nodes[node] = value

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].add(to_node)
        self.distances[(from_node, to_node)] = distance


PATTERN = re.compile(
    r"Valve ([A-Z]{2}) has flow rate=(\d+); " "tunnels? leads? to valves? ([A-Z ,]+)"
)


def load_data(path):
    with open(path) as f:
        rows = [PATTERN.fullmatch(row).groups() for row in f.read().strip().split("\n")]
    valves = {valve: (int(rate), dest.split(", ")) for valve, rate, dest in rows}
    return reduce_graph(valves)


def reduce_graph(valves):
    g = Graph()
    for valve, (flow_rate, nbrs) in valves.items():
        if flow_rate == 0 and valve != "AA":
            continue
        g.add_node(valve, flow_rate)
        for nbr in nbrs:
            prev = valve
            steps = 1
            while not (valves[nbr][0] != 0 or nbr == "AA"):
                prev, nbr = nbr, next(n for n in valves[nbr][1] if n != prev)
                steps += 1
            g.add_node(nbr, valves[nbr][0])
            g.add_edge(valve, nbr, steps)

    return g


def get_value(graph):
    node_index = {n: 1 << i for i, n in enumerate(graph.nodes)}

    @cache
    def value(loc, remaining, open_valves):
        if remaining <= 0:
            return 0

        values = []
        if (open_valves & node_index[loc]) == 0:
            values.append(
                remaining * graph.nodes[loc]
                + value(loc, remaining - 1, open_valves | node_index[loc])
            )

        for nbr in graph.edges[loc]:
            dist = graph.distances[(loc, nbr)]
            values.append(value(nbr, remaining - dist, open_valves))

        return max(values)

    return value


def part_1(graph: Graph):
    value = get_value(graph)
    return value("AA", 29, 0)


def part_2(graph):
    value = get_value(graph)
    n_nodes = len(graph.nodes)
    all_open = (1 << n_nodes) - 1

    max_value = float("-inf")

    for open1 in range(all_open):
        open2 = all_open - open1
        max_value = max(max_value, value("AA", 25, open1) + value("AA", 25, open2))

    return max_value


if __name__ == "__main__":
    graph = load_data(sys.argv[1])
    print(f"Part 1: {part_1(graph)}")
    print(f"Part 2: {part_2(graph)}")
