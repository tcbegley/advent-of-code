import sys
from heapq import heappop, heappush


def load_data(path):
    with open(path) as f:
        rows = f.readlines()

    targets = {}
    ducts = set()

    for y, row in enumerate(rows):
        for x, c in enumerate(row.strip()):
            if c != "#":
                ducts.add((x, y))
                if c != ".":
                    targets[(x, y)] = int(c)

    return targets, ducts


def l1(loc1, loc2):
    x1, y1 = loc1
    x2, y2 = loc2
    return abs(x1 - x2) + abs(y1 - y2)


def get_neighbours(loc, ducts):
    dirs = ((-1, 0), (1, 0), (0, -1), (0, 1))
    x, y = loc
    for dx, dy in dirs:
        if (x + dx, y + dy) in ducts:
            yield x + dx, y + dy


def lower_bound(loc, visited, targets):
    return min(
        (
            l1(loc, target)
            for target, i in targets.items()
            if (visited >> i) & 1 == 0
        ),
        default=0,
    )


def astar(targets, ducts, return_to_zero=False):
    target_lookup = {v: k for k, v in targets.items()}
    start = target_lookup[0]
    steps = {(start, 1): 0}
    queue = []
    heappush(queue, (lower_bound(start, 1, targets), start, 1))
    end_state = sum(1 << i for i in targets.values())

    while queue:
        _, loc, visited = heappop(queue)
        s = steps[(loc, visited)]

        if visited == end_state:
            return s

        for nbr in get_neighbours(loc, ducts):
            if nbr in targets:
                new_visited = visited | (1 << targets[nbr])
                if (
                    return_to_zero
                    and targets[nbr] != 0
                    and new_visited == end_state
                ):
                    new_visited ^= 1
            else:
                new_visited = visited
            if (nbr, new_visited) not in steps or steps[
                (nbr, new_visited)
            ] > s + 1:
                steps[(nbr, new_visited)] = s + 1
                heappush(
                    queue,
                    (
                        s + 1 + lower_bound(nbr, new_visited, targets),
                        nbr,
                        new_visited,
                    ),
                )


def part_1(targets, ducts):
    return astar(targets, ducts)


def part_2(targets, ducts):
    return astar(targets, ducts, return_to_zero=True)


if __name__ == "__main__":
    targets, ducts = load_data(sys.argv[1])
    print(f"Part 1: {part_1(targets, ducts)}")
    print(f"Part 2: {part_2(targets, ducts)}")
