import sys
from collections import defaultdict


def load_data(path):
    with open(path) as f:
        lines = f.read().strip().split("\n")
    return [[int(i) for i in line.split(": ")] for line in lines]


def part_1(lines):
    layers = defaultdict(lambda: 0)
    for line in lines:
        layers[line[0]] = line[1] * 2 - 2

    severity = 0
    for i in range(max(layers.keys()) + 1):
        if layers[i] and i % layers[i] == 0:
            severity += i * (layers[i] + 2) // 2
    return severity


def part_2(lines):
    layers = defaultdict(lambda: 0)
    for line in lines:
        layers[line[0]] = line[1] * 2 - 2

    delay = 0
    while True:
        for i in range(max(layers.keys()) + 1):
            if layers[i] and (i + delay) % layers[i] == 0:
                caught = True
                break
        if not caught:
            break
        else:
            caught = False
            delay += 1

    return delay


if __name__ == "__main__":
    lines = load_data(sys.argv[1])
    print(f"Part 1: {part_1(lines)}")
    print(f"Part 2: {part_2(lines)}")
