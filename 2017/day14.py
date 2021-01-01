import sys
from collections import defaultdict
from functools import reduce


class Graph:
    def __init__(self):
        self.graph = defaultdict(set)

    def add_edge(self, u, v):
        self.graph[u].add(v)
        self.graph[v].add(u)

    def bfs(self, start):
        visited = set()

        queue = [start]
        visited.add(start)

        while queue:
            s = queue.pop(0)
            for i in self.graph[s]:
                if i not in visited:
                    visited.add(i)
                    queue.append(i)
        return visited


class WrappedList:
    def __init__(self, lst):
        self.list_ = lst[:]
        self.n = len(lst)

    def __getitem__(self, i):
        if isinstance(i, slice):
            start = i.start % self.n
            stop = i.stop % self.n
            if start >= stop:
                return self.list_[start:] + self.list_[:stop]
            return self.list_[start:stop]
        return self.list_[i % self.n]

    def __setitem__(self, i, v):
        if isinstance(i, slice):
            start = i.start % self.n
            stop = i.stop % self.n
            if start >= stop:
                self.list_[start:] = v[: self.n - start]
                self.list_[:stop] = v[self.n - start :]
            else:
                self.list_[start:stop] = v
        else:
            self.list_[i % self.n] = v


def load_data(path):
    with open(path) as f:
        return f.read().strip()


def densify(nums):
    return reduce(lambda x, y: x ^ y, nums)


def knot_hash(hash_input):
    lengths = list(map(ord, hash_input)) + [17, 31, 73, 47, 23]
    w = WrappedList(list(range(256)))
    skip = 0
    pos = 0
    for _ in range(64):
        for length in lengths:
            if length > 1:
                w[pos : pos + length] = list(reversed(w[pos : pos + length]))
            pos += length + skip
            skip += 1
    dense = [densify(w[16 * i : 16 * (i + 1)]) for i in range(16)]
    return "".join([bin(x)[2:].zfill(8) for x in dense])


def part_1(hash_input):
    hashes = []
    for i in range(128):
        hashes.append(
            sum(int(j) for j in knot_hash("{}-{}".format(hash_input, i)))
        )
    return sum(hashes)


def part_2(hash_input):
    hashes = []
    for i in range(128):
        hashes.append(
            [int(j) for j in knot_hash("{}-{}".format(hash_input, i))]
        )

    g = Graph()
    to_visit = set()
    for i in range(128):
        for j in range(128):
            if hashes[i][j]:
                to_visit.add((i, j))
                g.add_edge((i, j), (i, j))
                if i > 0 and hashes[i - 1][j]:
                    g.add_edge((i, j), (i - 1, j))
                if j < 127 and hashes[i][j + 1]:
                    g.add_edge((i, j), (i, j + 1))
                if i < 127 and hashes[i + 1][j]:
                    g.add_edge((i, j), (i + 1, j))
                if j < 127 and hashes[i][j + 1]:
                    g.add_edge((i, j), (i, j + 1))

    count = 0
    while to_visit:
        count += 1
        to_visit -= g.bfs(next(iter(to_visit)))
    return count


if __name__ == "__main__":
    hash_ = load_data(sys.argv[1])
    print(f"Part 1: {part_1(hash_)}")
    print(f"Part 2: {part_2(hash_)}")
