import sys
from collections import Counter


class Cart:
    FS_LOOKUP = {
        (1, 0): (0, -1),
        (-1, 0): (0, 1),
        (0, 1): (-1, 0),
        (0, -1): (1, 0),
    }
    BS_LOOKUP = {
        (1, 0): (0, 1),
        (-1, 0): (0, -1),
        (0, 1): (1, 0),
        (0, -1): (-1, 0),
    }
    PLUS_LOOKUP = {
        (1, 0): [(0, -1), (1, 0), (0, 1)],
        (-1, 0): [(0, 1), (-1, 0), (0, -1)],
        (0, 1): [(1, 0), (0, 1), (-1, 0)],
        (0, -1): [(-1, 0), (0, -1), (1, 0)],
    }

    def __init__(self, d, l):
        self.dir = d
        self.loc = l
        self._dir_changes = 0

    def move(self, track):
        self.loc = self.add(self.loc, self.dir)
        try:
            c = track[self.loc]
        except KeyError:
            raise KeyError("CART DERAILED")

        self.change_dir(c)

    def change_dir(self, c):
        if c == "/":
            self.dir = self.FS_LOOKUP[self.dir]
        elif c == "\\":
            self.dir = self.BS_LOOKUP[self.dir]
        elif c == "+":
            self.dir = self.PLUS_LOOKUP[self.dir][self._dir_changes % 3]
            self._dir_changes += 1

    @staticmethod
    def add(a, b):
        """add tuples"""
        return (a[0] + b[0], a[1] + b[1])


def print_track(track, carts=None):
    dir_map = {(1, 0): ">", (0, -1): "^", (0, 1): "v", (-1, 0): "<"}

    maxi = max(track.keys(), key=lambda x: x[0])[0]
    maxj = max(track.keys(), key=lambda x: x[1])[1]

    if carts is not None:
        cart_locs = {c.loc: dir_map[c.dir] for c in carts}
    else:
        cart_locs = {}

    for j in range(maxj + 1):
        row = ""
        for i in range(maxi + 1):
            if (i, j) in cart_locs:
                row += cart_locs[(i, j)]
            elif (i, j) in track:
                row += track[(i, j)]
            else:
                row += "."
        print(row)


def check_for_crash(carts):
    most_common = Counter([c.loc for c in carts]).most_common(1)[0]
    if most_common[1] > 1:
        return most_common[0]
    return False


def answer(path):
    with open(path) as f:
        lines = f.read().split("\n")

    track = {}
    carts = []

    for j, line in enumerate(lines):
        for i, c in enumerate(line):
            if c in "-|/\\+":
                track[(i, j)] = c
            elif c in "v^":
                track[(i, j)] = "|"
                if c == "v":
                    carts.append(Cart((0, 1), (i, j)))
                else:
                    carts.append(Cart((0, -1), (i, j)))
            elif c in "<>":
                track[(i, j)] = "-"
                if c == ">":
                    carts.append(Cart((1, 0), (i, j)))
                else:
                    carts.append(Cart((-1, 0), (i, j)))

    while True:
        for c in sorted(carts, key=lambda c: (c.loc[1], c.loc[0])):
            c.move(track)

        crash = check_for_crash(carts)
        if crash:
            return crash


if __name__ == "__main__":
    print(answer(sys.argv[1]))
