import sys
from collections import defaultdict


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = defaultdict(set)

    def add_edge(self, node1, node2):
        self.nodes[node1] = node1 == node1.lower()
        self.nodes[node2] = node2 == node2.lower()
        self.edges[node1].add(node2)
        self.edges[node2].add(node1)

    def search(self, allow_single_revisit=False):
        count = 0
        visited = {"start"}
        small_cave_revisited = False

        def backtrack(start="start"):
            if start == "end":
                nonlocal count
                count += 1
            else:
                for nbr in self.edges[start]:
                    if self.nodes[nbr]:
                        nonlocal small_cave_revisited
                        if nbr not in visited:
                            visited.add(nbr)
                            backtrack(nbr)
                            visited.remove(nbr)
                        elif (
                            allow_single_revisit
                            and not small_cave_revisited
                            and nbr not in {"start", "end"}
                        ):
                            # in part 2 we can revisit at most one small cave
                            # as long as it isn't the start or end
                            small_cave_revisited = True
                            backtrack(nbr)
                            small_cave_revisited = False
                    elif not self.nodes[nbr]:
                        # large cave, can be revisited
                        backtrack(nbr)

        backtrack()
        return count


def load_data(path):
    caves = Graph()

    with open(path) as f:
        edges = [line.strip().split("-") for line in f.readlines()]

    for node1, node2 in edges:
        caves.add_edge(node1, node2)

    return caves


def part_1(caves):
    return caves.search()


def part_2(caves):
    return caves.search(allow_single_revisit=True)


if __name__ == "__main__":
    caves = load_data(sys.argv[1])
    print(f"Part 1: {part_1(caves)}")
    print(f"Part 2: {part_2(caves)}")
