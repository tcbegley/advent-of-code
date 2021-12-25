import sys
from collections import deque


def load_data(path):
    with open(path) as f:
        return int(f.read().strip())


def part_1(data):
    elves = deque(range(1, data + 1))

    for _ in range(len(elves) - 1):
        elves.rotate(-1)
        elves.popleft()

    return elves[0]


def part_2(data):
    elves = deque(range(1, data + 1))
    rotate = len(elves) % 2 == 1
    elves.rotate(-(len(elves) // 2))

    for _ in range(len(elves) - 1):
        elves.popleft()
        if rotate:
            elves.rotate(-1)
            rotate = False
        else:
            rotate = True

    return elves[0]


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
