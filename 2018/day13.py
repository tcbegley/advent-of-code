import sys
from copy import deepcopy


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

    def __init__(self, location, direction):
        self.loc = location
        self.dir = direction
        self._dir_changes = 0
        self._alive = True

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


def load_data(path):
    with open(path) as f:
        rows = f.read().split("\n")

    track = {}
    carts = []

    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            if char in "-|/\\+":
                track[(x, y)] = char
            elif char == "v":
                track[(x, y)] = "|"
                carts.append(Cart((x, y), (0, 1)))
            elif char == "^":
                track[(x, y)] = "|"
                carts.append(Cart((x, y), (0, -1)))
            elif char == ">":
                track[(x, y)] = "-"
                carts.append(Cart((x, y), (1, 0)))
            elif char == "<":
                track[(x, y)] = "-"
                carts.append(Cart((x, y), (-1, 0)))

    return track, carts


def part_1(track, carts):
    while True:
        for cart in sorted(carts, key=lambda c: (c.loc[1], c.loc[0])):
            cart.move(track)
            if any(cart2.loc == cart.loc for cart2 in carts if cart is not cart2):
                return cart.loc


def part_2(track, carts):
    while len(carts) > 1:
        for cart in sorted(carts, key=lambda c: (c.loc[1], c.loc[0])):
            if not cart._alive:
                continue
            cart.move(track)
            for cart2 in carts:
                if cart is cart2:
                    continue
                elif cart2._alive and (cart.loc == cart2.loc):
                    cart._alive = False
                    cart2._alive = False

        carts = [cart for cart in carts if cart._alive]

    return carts[0].loc


if __name__ == "__main__":
    track, carts = load_data(sys.argv[1])
    print(f"Part 1: {part_1(track, deepcopy(carts))}")
    print(f"Part 2: {part_2(track, carts)}")
