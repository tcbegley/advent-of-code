import sys
from collections import deque

DIR_LOOKUP = {"N": 1j, "E": 1, "S": -1j, "W": -1}


class Graph:
    def __init__(self):
        self.vertices = set()
        self.edges = {}

    def add_edge(self, start, end):
        self.vertices.update((start, end))
        self.edges.setdefault(start, set()).add(end)
        self.edges.setdefault(end, set()).add(start)


def bfs(graph, start=0j, threshold=1_000):
    visited = {start}
    queue = deque([(start, 0)])
    count = 0

    while queue:
        loc, n_steps = queue.popleft()
        count += n_steps >= threshold

        for nbr in graph.edges[loc]:
            if nbr not in visited:
                visited.add(nbr)
                queue.append((nbr, n_steps + 1))

    # because we are doing breadth-first search, n_steps is the max steps taken
    return n_steps, count


def load_data(path):
    with open(path) as f:
        return f.read().strip()


def create_graph(data):
    graph = Graph()

    # set of current locations
    locs = {0j}
    # stack will contain start points and end points computed so far in the group
    stack = []

    for c in data:
        if c in "NESW":
            # move in the direction c from all current locations, adding edges to graph
            locs = {
                graph.add_edge(loc, new_loc := loc + DIR_LOOKUP[c]) or new_loc
                for loc in locs
            }
        elif c == "(":
            # entering a new group, record current locations as start points and add
            # an empty set to keep track of the end points as we compute them
            stack.append((set(locs), set()))
        elif c == ")":
            # leaving a group, the end points we calculated become the new locations
            stack[-1][1].update(locs)
            _, locs = stack.pop()
        elif c == "|":
            # starting a new alternative in the group, update the end points with the
            # current locations, then return to the starting locations
            stack[-1][1].update(locs)
            locs = stack[-1][0]

    return graph


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    max_steps, door_count = bfs(create_graph(data))
    print(f"Part 1: {max_steps}")
    print(f"Part 2: {door_count}")
