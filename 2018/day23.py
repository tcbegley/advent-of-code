import re
import sys
from operator import itemgetter

NUMBER_PATTERN = re.compile(r"-?[\d]+")


def process_row(row):
    x, y, z, r = map(int, NUMBER_PATTERN.findall(row))
    return (x, y, z), r


def load_data(path):
    with open(path) as f:
        return [process_row(row) for row in f.read().strip().split("\n")]


def l1(loc1, loc2):
    return sum(abs(a - b) for a, b in zip(loc1, loc2))


def part_1(data):
    loc_max, r_max = max(data, key=itemgetter(1))
    return sum(l1(loc_max, loc) <= r_max for loc, _ in data)


r"""
An L1 ball in 3D is characterised by

|x - x0| + |y - y0| + |z - z0| <= r

The boundary of which is therefore characterised by 8 planes with the equations

(x - x0) + (y - y0) + (z - z0) = +/-r
(x - x0) + (y - y0) - (z - z0) = +/-r
(x - x0) - (y - y0) + (z - z0) = +/-r
-(x - x0) + (y - y0) + (z - z0) = +/-r

In other words, by defining
(a, b, c, d) = (x + y + z, x + y - z, x - y + z, -x + y + z)
we can characterise the 3D L1 ball in terms of the 4D L^\infty ball

|a - a0| <= r, |b - b0| <= r, |c - c0| <= r, |d - d0| <= r

where a0 = x0 + y0 + z0 etc.

The L^\infty balls are easy to intersect, so we can work in that space and then map
back.
"""


class Ball3:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z

        self.r = r


class Ball4:
    def __init__(self, a_range, b_range, c_range, d_range):
        self.a_range = a_range
        self.b_range = b_range
        self.c_range = c_range
        self.d_range = d_range

    def __and__(self, other):
        a_range = (
            min(self.a_range[0], other.a_range[0]),
            max(self.a_range[1], other.a_range[1]),
        )
        b_range = (
            min(self.b_range[0], other.b_range[0]),
            max(self.b_range[1], other.b_range[1]),
        )
        c_range = (
            min(self.c_range[0], other.c_range[0]),
            max(self.c_range[1], other.c_range[1]),
        )
        d_range = (
            min(self.d_range[0], other.d_range[0]),
            max(self.d_range[1], other.d_range[1]),
        )
        return self.__class__(
            a_range=a_range, b_range=b_range, c_range=c_range, d_range=d_range
        )

    @property
    def non_empty(self):
        return all(
            low <= high
            for low, high in [self.a_range, self.b_range, self.c_range, self.d_range]
        )


def part_2(data):
    pass


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
