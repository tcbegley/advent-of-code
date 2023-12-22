import sys
from collections import defaultdict, deque, namedtuple

Point = namedtuple("Point", ["x", "y", "z"])
Brick = namedtuple("Brick", ["start", "end"])


def process_row(row):
    start, end = sorted([Point(*map(int, p.split(","))) for p in row.split("~")])
    return Brick(start, end)


def load_data(path):
    with open(path) as f:
        rows = f.read().strip().split("\n")

    return [process_row(row) for row in rows]


def part_1(data):
    queue = deque(data)
    max_height = defaultdict(int)

    while queue:
        brick = queue.popleft()
        coords = [
            (x, y)
            for x in range(brick.start.x, brick.end.x + 1)
            for y in range(brick.start.y, brick.end.y + 1)
        ]
        height = max(max_height[coord] for coord in coords)
        for coord in coords:
            max_height[coord] = height + (brick.end.z - brick.start.z) + 1

    return max_height


def part_2(data):
    pass


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
