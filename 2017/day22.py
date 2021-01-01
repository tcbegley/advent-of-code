import sys
from collections import defaultdict


class Carrier:
    dirs = {"n": (-1, 0), "s": (1, 0), "e": (0, 1), "w": (0, -1)}
    left = dict(zip("nesw", "wnes"))
    right = dict(zip("nesw", "eswn"))
    new_dir = {
        ".": dict(zip("nesw", "wnes")),
        "W": dict(zip("nesw", "nesw")),
        "#": dict(zip("nesw", "eswn")),
        "F": dict(zip("nesw", "swne")),
    }
    update = dict(zip(".W#F", "W#F."))

    def __init__(self, m):
        self.cur_dir = "n"
        self.x = 0
        self.y = 0
        self.world = defaultdict(lambda: ".")
        self.initialise_world(m)
        self.infected = 0

    def initialise_world(self, m):
        r = len(m)
        c = len(m[0])
        for i in range(r):
            for j in range(c):
                self.world[(i - r // 2, j - c // 2)] = m[i][j]

    def move1(self):
        cur_loc = self.world[(self.x, self.y)]
        if cur_loc == ".":
            self.cur_dir = Carrier.left[self.cur_dir]
            self.world[(self.x, self.y)] = "#"
            self.infected += 1
        else:
            self.cur_dir = Carrier.right[self.cur_dir]
            self.world[(self.x, self.y)] = "."
        self.x, self.y = [
            x + y for x, y in zip((self.x, self.y), Carrier.dirs[self.cur_dir])
        ]

    def move2(self):
        cur_loc = self.world[(self.x, self.y)]
        self.cur_dir = Carrier.new_dir[cur_loc][self.cur_dir]
        self.world[(self.x, self.y)] = Carrier.update[cur_loc]
        if cur_loc == "W":
            self.infected += 1
        self.x, self.y = [
            x + y for x, y in zip((self.x, self.y), Carrier.dirs[self.cur_dir])
        ]


def load_data(path):
    with open(path) as f:
        return f.read().strip().split("\n")


def part_1(map_):
    c = Carrier(map_)
    for _ in range(10_000):
        c.move1()
    return c.infected


def part_2(map_):
    c = Carrier(map_)
    for _ in range(10_000_000):
        c.move2()
    return c.infected


if __name__ == "__main__":
    map_ = load_data(sys.argv[1])
    print(f"Part 1: {part_1(map_)}")
    print(f"Part 2: {part_2(map_)}")
