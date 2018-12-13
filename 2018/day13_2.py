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

    def __init__(self, d, l, i):
        self.id = i
        self.dir = d
        self.loc = l
        self._dir_changes = 0
        self.alive = True

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
        cart_locs = {c.loc: dir_map[c.dir] for c in carts if c.alive}
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


def check_for_crashes(carts):
    most_common = Counter([c.loc for c in carts if c.alive]).most_common()

    for c in carts:
        if c.loc == most_common[0] and most_common[1] > 1:
            c.alive = False


def answer(path):
    with open(path) as f:
        lines = f.read().split("\n")

    track = {}
    carts = []
    _id = 0

    for j, line in enumerate(lines):
        for i, c in enumerate(line):
            if c in "-|/\\+":
                track[(i, j)] = c
            elif c in "v^":
                track[(i, j)] = "|"
                if c == "v":
                    carts.append(Cart((0, 1), (i, j), _id))
                    _id += 1
                else:
                    carts.append(Cart((0, -1), (i, j), _id))
                    _id += 1
            elif c in "<>":
                track[(i, j)] = "-"
                if c == ">":
                    carts.append(Cart((1, 0), (i, j), _id))
                    _id += 1
                else:
                    carts.append(Cart((-1, 0), (i, j), _id))
                    _id += 1

    while len([c for c in carts if c.alive]) > 1:
        for c in sorted(carts, key=lambda c: (c.loc[0], c.loc[1])):
            if not c.alive:
                continue
            c.move(track)
            for c2 in carts:
                if c.id == c2.id:
                    continue
                elif c2.alive and (c.loc == c2.loc):
                    c.alive = False
                    c2.alive = False
                    break

    cart = [c for c in carts if c.alive][0]
    return cart.loc


if __name__ == "__main__":
    print(answer(sys.argv[1]))
