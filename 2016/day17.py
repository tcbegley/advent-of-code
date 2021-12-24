import sys
from hashlib import md5
from heapq import heappop, heappush


def load_data(path):
    with open(path) as f:
        return f.read().strip()


def get_hash(passcode, path):
    return md5(f"{passcode}{path}".encode()).hexdigest()


def l1(loc1, loc2):
    return sum(abs(a - b) for a, b in zip(loc1, loc2))


def get_neighbours(loc, passcode, path):
    x, y = loc
    dirs = [("U", (0, -1)), ("D", (0, 1)), ("L", (-1, 0)), ("R", (1, 0))]
    h = get_hash(passcode, path)
    for c, (d, (dx, dy)) in zip(h, dirs):
        if c in "bcdef" and 0 <= x + dx <= 3 and 0 <= y + dy <= 3:
            yield d, (x + dx, y + dy)


def a_star(passcode, find_longest=False):
    start, target = (0, 0), (3, 3)

    queue = []
    visited = {("", start)}
    heappush(queue, (l1(start, target), "", start))

    max_len = 0

    while queue:
        _, path, loc = heappop(queue)

        if loc == target:
            if not find_longest:
                return path
            max_len = max(max_len, len(path))
            continue

        for d, nbr in get_neighbours(loc, passcode, path):
            if (path + d, nbr) not in visited:
                visited.add((path + d, nbr))
                priority = len(path) + 1 + l1(nbr, target)
                heappush(queue, (priority, path + d, nbr))

    return max_len


def part_1(passcode):
    return a_star(passcode)


def part_2(data):
    return a_star(passcode, find_longest=True)


if __name__ == "__main__":
    passcode = load_data(sys.argv[1])
    print(f"Part 1: {part_1(passcode)}")
    print(f"Part 2: {part_2(passcode)}")
