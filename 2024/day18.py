import sys
from heapq import heappop, heappush


def load_data(path):
    def process_line(line):
        x, y = line.split(",")
        return int(x), int(y)

    with open(path) as f:
        return [process_line(line) for line in f.read().strip().split("\n")]


def search(corrupted, target=(70, 70)):
    queue = [(140, 0, (0, 0))]
    seen = {(0, 0)}

    while queue:
        _, n_steps, loc = heappop(queue)
        if loc == target:
            return n_steps
        for d in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if (
                (next_loc := (loc[0] + d[0], loc[1] + d[1])) not in seen
                and next_loc not in corrupted
                and 0 <= next_loc[0] <= 70
                and 0 <= next_loc[1] <= 70
            ):
                seen.add(next_loc)
                dist = sum(target) - sum(next_loc)
                heappush(queue, (dist + n_steps + 1, n_steps + 1, next_loc))


def part_1(data):
    corrupted = set(data[:1024])
    return search(corrupted)


def part_2(data):
    for i in range(1025, len(data)):
        corrupted = set(data[:i])
        if search(corrupted) is None:
            return ",".join(map(str, data[i - 1]))


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
