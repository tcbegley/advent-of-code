import sys
from functools import reduce
from operator import mul


class UnionFind:
    def __init__(self, locs):
        self.num_components = len(locs)
        self._root = {loc: loc for loc in locs}
        self._size = {loc: 1 for loc in locs}

    def find(self, loc):
        root = loc
        while self._root[root] != root:
            root = self._root[root]

        # path compression
        while loc != root:
            next_ = self._root[loc]
            self._root[loc] = root
            loc = next_

        return root

    def unify(self, loc1, loc2):
        root1 = self.find(loc1)
        root2 = self.find(loc2)

        if root1 != root2:
            if self._size[root1] < self._size[root2]:
                self._size[root2] += self._size[root1]
                self._root[root1] = root2
            else:
                self._size[root1] += self._size[root2]
                self._root[root2] = root1

            self.num_components -= 1

    def component_sizes(self):
        roots = set(self._root.values())
        return [self._size[root] for root in roots]


def load_data(path):
    with open(path) as f:
        return [tuple(map(int, row.split(","))) for row in f.read().strip().split("\n")]


def l2(loc1, loc2):
    # no point in sqrting because we only care about ordering, not actual value
    return sum((a - b) ** 2 for a, b in zip(loc1, loc2))


def main(data):
    distances = {}
    for loc1 in data:
        for loc2 in data:
            if loc1 < loc2:
                distances[loc1, loc2] = l2(loc1, loc2)

    union_find = UnionFind(data)

    for count, (_, (loc1, loc2)) in enumerate(
        sorted((v, k) for k, v in distances.items())
    ):
        if count == 1000:
            # after 1000 connections, can calucate part 1 answer
            part_1 = reduce(mul, sorted(union_find.component_sizes(), reverse=True)[:3])
        union_find.unify(loc1, loc2)

        if union_find.num_components == 1:
            # once we have a single large component, calculate part 2 and break
            part_2 = loc1[0] * loc2[0]
            break

    return part_1, part_2


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    part_1, part_2 = main(data)
    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")
