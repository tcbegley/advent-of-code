import sys
from itertools import product


class Box:
    def __init__(self, loc1, loc2):
        self.x_low = min(loc1[0], loc2[0])
        self.x_high = max(loc1[0], loc2[0])
        self.y_low = min(loc1[1], loc2[1])
        self.y_high = max(loc1[1], loc2[1])

        loc1, loc2 = sorted(loc1, loc2)
        self.m = (loc2[1] - loc1[1]) / (loc2[0] - loc1[0])
        self.loc1 = loc1

    def __contains__(self, loc):
        return (self.x_low <= loc[0] <= self.x_high) and (
            self.y_low <= loc[1] <= self.y_high
        )

    def is_above_diag(self, loc):
        return loc[1] - self.loc1[1] >= self.m * (loc[0] - self.loc1[0])


class Polygon:
    def __init__(self, vertices):
        n = len(vertices)
        vlines = []
        hlines = []

        for i in range(len(vertices)):
            (x1, y1) = vertices[i]
            (x2, y2) = vertices[(i + 1) % n]

            if x1 == x2:
                vlines.append((x1, *sorted([y1, y2])))
            else:
                hlines.append((y1, *sorted([x1, x2])))

        self.vlines = vlines
        self.hlines = hlines

    def __contains__(self, loc):
        # draw a straight line from (x, y) to (\infty, y) and count how many times you
        # cross a border. If it's an even number then we must have started outside,
        # otherwise we must have started inside.

        # the annoying edge case is if you pass through an endpoint, then it depends on
        # what the line is doing
        #
        #       #......#      #.......
        #       #......#   >  ########
        #    >  ########      .......#
        #
        # on the left, passing through the two endpoints is like crossing the border
        # twice, on the right it's like crossing the border once.
        x, y = loc


def load_data(path):
    with open(path) as f:
        return [tuple(map(int, row.split(","))) for row in f.read().strip().split("\n")]


def part_1(data):
    return max(
        (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        for (x1, y1), (x2, y2) in product(data, data)
    )


def check_box(box, i, j, data):
    n = len(data)
    for k in range(j):
        loc = data[(i + k) % n]
        if loc in box:
            return False

    for k in range(j, n):
        loc = data[(i + k) % n]

    return True


def part_2(data):
    n = len(data)
    for i, loc1 in enumerate(data):
        for j in range(1, n):
            loc2 = data[(i + j) % n]
            box = Box(loc1, loc2)


# def part_2(data):
#     idx = data.index(min(data))
#     data = data[idx:] + data[:idx]

#     # keep track of where interior is on each vertex
#     data_with_ptrs = [(data[0], (1, 1))]
#     n = len(Data)
#     for i, loc in enumerate(data[1:], start=1):
#         prev, ptr = data_with_ptrs[-1]
#         next_ = data[(i + 1) % n]


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
