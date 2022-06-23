import sys
from collections import deque


class UnionFind:
    def __init__(self, x_range, y_range):
        x_min, x_max = x_range
        y_min, y_max = y_range

        self.num_components = (x_max - x_min + 1) * (y_max - y_min + 1) + 1
        self.id = {
            (x, y): (x, y)
            for x in range(x_min, x_max + 1)
            for y in range(y_min, y_max + 1)
        }
        self.id[None] = None
        self.size = {
            (x, y): 1
            for x in range(x_min, x_max + 1)
            for y in range(y_min, y_max + 1)
        }
        self.size[None] = 1

    def find(self, loc):
        root = loc
        while root != self.id[root]:
            root = self.id[root]

        # path compression
        while loc != root:
            next_ = self.id[loc]
            self.id[loc] = root
            loc = next_

        return root

    def component_size(self, loc):
        return self.size[self.find(loc)]

    def unify(self, loc1, loc2):
        root1 = self.find(loc1)
        root2 = self.find(loc2)

        if root1 != root2:
            if root2 is None or (
                root1 is not None and self.size[root1] < self.size[root2]
            ):
                self.size[root2] += self.size[root1]
                self.id[root1] = root2
            else:
                self.size[root1] += self.size[root2]
                self.id[root2] = root1

            self.num_components -= 1


def load_data(path):
    with open(path) as f:
        return [tuple(map(int, row.split(","))) for row in f.readlines()]


def get_neighbours(x, y, x_min, x_max, y_min, y_max):
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if x_min <= x + dx <= x_max and y_min <= y + dy <= y_max:
            yield x + dx, y + dy


def part_1(coords):
    x_min, x_max = (
        min(coords, key=lambda c: c[0])[0],
        max(coords, key=lambda c: c[0])[0],
    )
    y_min, y_max = (
        min(coords, key=lambda c: c[1])[1],
        max(coords, key=lambda c: c[1])[1],
    )

    queue = deque(coords)
    next_queue = deque()
    visited_this_iteration = set()
    grid = {}

    while queue:
        pass


def part_2(coords):
    pass


if __name__ == "__main__":
    coords = load_data(sys.argv[1])
    print(f"Part 1: {part_1(coords)}")
    print(f"Part 2: {part_2(coords)}")
