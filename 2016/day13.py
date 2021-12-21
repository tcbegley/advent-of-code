import heapq
import sys
from collections import deque
from functools import cache


def load_data(path):
    with open(path) as f:
        return int(f.read().strip())


def count_bits(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count


@cache
def is_open(x, y, n):
    return count_bits(x * x + 3 * x + 2 * x * y + y + y * y + n) % 2 == 0


def l1(loc1, loc2):
    x1, y1 = loc1
    x2, y2 = loc2
    return abs(x1 - x2) + abs(y1 - y2)


def get_neighbours(x, y, n):
    nbr_dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for dx, dy in nbr_dirs:
        if x + dx >= 0 and y + dy >= 0 and is_open(x + dx, y + dy, n):
            yield (x + dx, y + dy)


def a_star(start, target, n):
    queue = []
    steps_taken = {start: 0}
    heapq.heappush(queue, (l1(start, target), start))

    while queue:
        _, (x, y) = heapq.heappop(queue)
        steps = steps_taken[(x, y)]

        if (x, y) == target:
            return steps

        for nbr in get_neighbours(x, y, n):
            if nbr not in steps_taken or steps_taken[nbr] > steps + 1:
                steps_taken[nbr] = steps + 1
                heapq.heappush(queue, (steps + 1 + l1(nbr, target), nbr))

    return None


def bfs(start, n, limit=50):
    queue, visited, steps = deque([start]), {start}, 0

    while steps < limit:
        next_queue = deque()
        while queue:
            loc = queue.popleft()
            for nbr in get_neighbours(loc[0], loc[1], n):
                if nbr not in visited:
                    visited.add(nbr)
                    next_queue.append(nbr)

        queue = next_queue
        steps += 1

    return visited


def part_1(n):
    return a_star((1, 1), (31, 39), n)


def part_2(n):
    return len(bfs((1, 1), n, limit=50))


if __name__ == "__main__":
    n = load_data(sys.argv[1])
    print(f"Part 1: {part_1(n)}")
    print(f"Part 2: {part_2(n)}")
