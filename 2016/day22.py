import re
import sys
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import permutations


@dataclass
class Node:
    size: int
    used: int

    @property
    def available(self):
        return self.size - self.used

    @property
    def usage(self):
        return self.available / self.size * 100


SPACE = re.compile(r"\s+")
FILESYSTEM = re.compile(r"/dev/grid/node-x(\d+)-y(\d+)")


def load_data(path):
    def process_line(line):
        filesystem, size, used, _, _ = SPACE.split(line.strip())
        x, y = FILESYSTEM.findall(filesystem)[0]
        return (int(x), int(y)), Node(
            size=int(size.rstrip("T")), used=int(used.rstrip("T"))
        )

    with open(path) as f:
        lines = f.readlines()

    return dict(map(process_line, lines[2:]))


def compatible(a, b):
    return 0 < a.used <= b.available


def part_1(nodes):
    return sum(compatible(a, b) for a, b in permutations(nodes.values(), 2))


def l1(loc1, loc2):
    (x1, y1), (x2, y2) = loc1, loc2
    return abs(x1 - x2) + abs(y1 - y2)


def get_empty(nodes):
    for empty, node in nodes.items():
        if node.used == 0:
            return empty


def get_neighbours(loc, compatible):
    dirs = ((-1, 0), (1, 0), (0, -1), (0, 1))
    x, y = loc

    for dx, dy in dirs:
        if (x + dx, y + dy) in compatible:
            yield (x + dx, y + dy)


def a_star(start, target, nodes):
    compatible_locs = {
        loc for loc, node in nodes.items() if compatible(node, nodes[start])
    }
    queue = []
    heappush(queue, (l1(start, target), start))
    steps = {start: 0}

    while queue:
        _, loc = heappop(queue)
        s = steps[loc]

        if loc == target:
            return s

        for nbr in get_neighbours(loc, compatible_locs):
            if nbr not in steps or steps[nbr] > s + 1:
                steps[nbr] = s + 1
                heappush(queue, (s + 1 + l1(start, target), nbr))


def part_2(nodes):
    max_x = max(x for x, _ in nodes)

    # This solution will not work on arbitrary input, but should work on any
    # particular user input. the following assert statement checks the
    # assumptions we're making hold.

    # assert that we have a clear line of sight to the target
    empty = get_empty(nodes)
    assert all(
        compatible(nodes[(x, 0)], nodes[empty])
        and compatible(nodes[(x, 1)], nodes[empty])
        for x in range(max_x + 1)
    )

    # solution is steps taken to get empty adjacent to data, plus 1 swap, plus
    # 5 times the number of spaces to move (takes 4 moves to move empty round
    # in front and then one more to swap it)
    steps = 0

    # steps to get empty to data
    steps += a_star(empty, (max_x - 1, 0), nodes)

    # perform first swap, so empty and data are still next to each other, but
    # data is on the left
    steps += 1

    # move data all the way to the origin, taking 5 steps for each place moved
    steps += 5 * (max_x - 1)

    return steps


if __name__ == "__main__":
    nodes = load_data(sys.argv[1])
    print(f"Part 1: {part_1(nodes)}")
    print(f"Part 2: {part_2(nodes)}")
