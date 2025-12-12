import sys
from bisect import bisect_right
from itertools import combinations
from operator import itemgetter


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

        self.vlines = sorted(vlines)  # sorted by x-coordinate for bisect
        self.vline_xs = [v[0] for v in self.vlines]  # precompute for bisect
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
        # twice, on the right it's like crossing the border once. this is actually
        # handled automatically if we include the smaller valued endpoint in the check,
        # but not the larger. in the first picture we include neither, in the second
        # we include exactly one
        x, y = loc

        # check if point lies on a hline
        for yline, x1, x2 in self.hlines:
            if y == yline and x1 <= x <= x2:
                return True

        inside = False
        # only check vlines with xline > x
        start = bisect_right(self.vline_xs, x)
        for _, y1, y2 in self.vlines[start:]:
            if (y >= y1) ^ (y >= y2):
                inside = not inside

        return inside

    def boundaries_intersect(self, loc1, loc2):
        # in addition to checking that all of the vertices of the square lie in the
        # polygon, we need to check that none of the edges of the square intersect an
        # edge of the polygon
        loc1, loc2 = sorted([loc1, loc2])
        x1, y1 = loc1
        x2, y2 = loc2
        if any(
            x1 < x < x2
            and (y_low <= min(y1, y2) < y_high or y_low < max(y1, y2) <= y_high)
            for x, y_low, y_high in self.vlines
        ):
            return True

        loc1, loc2 = sorted([loc1, loc2], key=itemgetter(1))
        x1, y1 = loc1
        x2, y2 = loc2
        return any(
            y1 < y < y2
            and (x_low <= min(x1, x2) < x_high or x_low < max(x1, x2) <= x_high)
            for y, x_low, x_high in self.hlines
        )


def load_data(path):
    with open(path) as f:
        return [tuple(map(int, row.split(","))) for row in f.read().strip().split("\n")]


def part_1(data):
    return max(
        (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
        for (x1, y1), (x2, y2) in combinations(data, 2)
    )


def part_2(data):
    polygon = Polygon(data)

    max_area = float("-inf")

    for (x1, y1), (x2, y2) in combinations(data, 2):
        if all(
            loc in polygon for loc in ((x1, y2), (x2, y1))
        ) and not polygon.boundaries_intersect((x1, y1), (x2, y2)):
            max_area = max(max_area, (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1))

    return max_area


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
