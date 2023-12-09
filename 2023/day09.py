import re
import sys

NUMBER = re.compile(r"-?\d+")


def load_data(path):
    with open(path) as f:
        return [
            list(map(int, row))
            for row in map(NUMBER.findall, f.read().strip().split("\n"))
        ]


def differences(sequence):
    for a, b in zip(sequence[:-1], sequence[1:]):
        yield b - a


def extrapolate(sequence, left=False):
    idx, mul = (0, -1) if left else (-1, 1)
    diffs = list(differences(sequence))
    if all(diff == 0 for diff in diffs):
        return sequence[idx]
    return sequence[idx] + mul * extrapolate(diffs, left=left)


def part_1(data):
    return sum(extrapolate(sequence) for sequence in data)


def part_2(data):
    return sum(extrapolate(sequence, left=True) for sequence in data)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
