import sys
from collections import defaultdict, deque, namedtuple
from itertools import chain

Point = namedtuple("Point", ["x", "y", "z"])
Brick = namedtuple("Brick", ["start", "end"])


def process_row(row):
    start, end = sorted([Point(*map(int, p.split(","))) for p in row.split("~")])
    return Brick(start, end)


def load_data(path):
    with open(path) as f:
        rows = f.read().strip().split("\n")

    return sorted((process_row(row) for row in rows), key=lambda brick: brick.start.z)


def drop_bricks(data):
    queue = deque(enumerate(data))
    # dictionary of id and height of current high-point for each (x, y) coord
    settled = defaultdict(lambda: (None, 0))
    supports = {}

    while queue:
        id_, brick = queue.popleft()
        coords = [
            (x, y)
            for x in range(brick.start.x, brick.end.x + 1)
            for y in range(brick.start.y, brick.end.y + 1)
        ]
        height = max(settled[coord][1] for coord in coords)
        supports[id_] = set(
            settled[coord][0] for coord in coords if settled[coord][1] == height
        )

        for coord in coords:
            settled[coord] = (id_, height + (brick.end.z - brick.start.z) + 1)

    return supports


def part_1(data):
    supports = drop_bricks(data)
    return len(data) - len(
        set(
            chain(
                *(
                    v
                    for v in supports.values()
                    if sum(id_ is not None for id_ in v) == 1
                )
            )
        )
    )


def part_2(data):
    count = 0
    for i in range(len(data)):
        supports = drop_bricks(data)
        queue = deque([i])

        while queue:
            id_ = queue.popleft()
            for next_id, v in supports.items():
                if id_ in v:
                    v.remove(id_)
                    if not v:
                        queue.append(next_id)
                        count += 1

    return count


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
