import re
import sys
from collections import defaultdict
from functools import lru_cache

COLOUR_PATTERN = re.compile(r"^(\d+) (.*) bags?$")


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


def make_bag_counter(rules):
    @lru_cache
    def count_bags(colour):
        if len(rules[colour]) == 0:
            # only this bag counts
            return 1
        return sum(cnt * count_bags(clr) for cnt, clr in rules[colour]) + 1

    return count_bags


def extract_colors(s):
    s = s.rstrip(".")
    if s == "no other bags":
        return []

    s = s.split(", ")
    s = [COLOUR_PATTERN.match(x) for x in s]
    return [(int(m.group(1)), m.group(2)) for m in s if m]


def load_data(path):
    with open(path) as f:
        rules = [r.split(" bags contain ") for r in f.read().strip().split("\n")]

    return [(r, extract_colors(s)) for r, s in rules]


def part_1(rules):
    g = Graph()

    for end, start_list in rules:
        for _, start in start_list:
            g.add_edge(start, end)

    return g.bfs("shiny gold") - 1  # don't count shiny gold bag


def part_2(rules):
    count_bags = make_bag_counter(dict(rules))
    return count_bags("shiny gold") - 1  # don't count the shiny gold one


if __name__ == "__main__":
    rules = load_data(sys.argv[1])
    print(f"Print 1: {part_1(rules)}")
    print(f"Print 2: {part_2(rules)}")
