import re
import sys
from collections import namedtuple


class Point(namedtuple("Point", ["x", "y"])):
    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)


UP = Point(0, -1)
DOWN = Point(0, 1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)

NUMBER = re.compile(r"\d+")


def load_data(path):
    with open(path) as f:
        rows = f.read().strip().split("\n")

    clay = set()
    for row in rows:
        fixed, low, high = map(int, NUMBER.findall(row))
        for z in range(low, high + 1):
            if row[0] == "x":
                clay.add(Point(fixed, z))
            else:
                clay.add(Point(z, fixed))

    return clay


def spread(loc, direction, clay, still):
    visited = set()
    while loc not in clay:
        visited.add(loc)
        locd = loc + DOWN
        if locd not in clay and locd not in still:
            return loc, visited
        loc += direction
    return None, visited


def fill(clay, source):
    ys = [y for _, y in clay]
    miny, maxy = min(ys), max(ys)

    falling = {source}
    spreading = set()

    flowing, still = set(), set()

    while falling or spreading:
        while falling:
            loc = falling.pop()
            while loc.y < maxy:
                locd = loc + DOWN
                if locd not in clay:
                    flowing.add(locd)
                    loc = locd
                else:
                    spreading.add(loc)
                    break

        while spreading:
            loc = spreading.pop()
            left, visited_left = spread(loc, LEFT, clay, still)
            right, visited_right = spread(loc, RIGHT, clay, still)
            if left is None and right is None:
                still.update(visited_left | visited_right)
                spreading.add(loc + UP)
            else:
                flowing.update(visited_left | visited_right)
                if left is not None:
                    falling.add(left)
                if right is not None and right != left:
                    falling.add(right)

    # filter out any water that isn't in the right range
    return {p for p in flowing if p.y >= miny}, {
        p for p in still if p.y >= miny
    }


def part_1(clay):
    flowing, still = fill(clay, Point(500, 0))
    return len(flowing | still)


def part_2(clay):
    _, still = fill(clay, Point(500, 0))
    return len(still)


if __name__ == "__main__":
    clay = load_data(sys.argv[1])
    print(f"Part 1: {part_1(clay)}")
    print(f"Part 2: {part_2(clay)}")
