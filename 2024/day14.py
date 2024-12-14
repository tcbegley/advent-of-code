import re
import sys
import time
from collections import Counter

NUMBER_PATTERN = re.compile(r"-?\d+")
MAX_X = 101
MAX_Y = 103


def process_line(line):
    px, py, vx, vy = map(int, NUMBER_PATTERN.findall(line))
    return (px, py), (vx, vy)


def load_data(path):
    with open(path) as f:
        return [process_line(line) for line in f.read().strip().split("\n")]


def update(positions):
    return [
        (((px + vx) % MAX_X, (py + vy) % MAX_Y), (vx, vy))
        for (px, py), (vx, vy) in positions
    ]


def part_1(data):
    quadrants = []
    for _ in range(100):
        data = update(data)
    for (px, py), _ in data:
        if px < MAX_X // 2:
            if py < MAX_Y // 2:
                quadrants.append(0)
            elif py > MAX_Y // 2:
                quadrants.append(1)
        elif px > MAX_X // 2:
            if py < MAX_Y // 2:
                quadrants.append(2)
            elif py > MAX_Y // 2:
                quadrants.append(3)
    total = 1
    for count in Counter(quadrants).values():
        total *= count

    return total


def visualise(data):
    positions = {(px, py) for (px, py), _ in data}
    print(
        "\n".join(
            "".join("X" if (x, y) in positions else "." for x in range(MAX_X))
            for y in range(MAX_Y)
        )
    )


def part_2(data):
    # this isn't very general, by printing out the grid I noticed that there was
    # something funny going on every 101 iterations, and then by printing out only
    # those + the iteration number I spotted the christmas tree eventually
    for i in range(20_000):
        data = update(data)
        if (i - 602) % 101 == 0:
            print(i)
            visualise(data)
            print()
            time.sleep(0.3)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
