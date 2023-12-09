import re
import sys
from itertools import pairwise

NUMBER = re.compile(r"-?\d+")


def load_data(path):
    with open(path) as f:
        return [
            list(map(int, row))
            for row in map(NUMBER.findall, f.read().strip().split("\n"))
        ]


def extrapolate(sequence, left=False):
    idx, mul = (0, -1) if left else (-1, 1)
    diffs = [b - a for a, b in pairwise(sequence)]
    if all(diff == 0 for diff in diffs):
        return sequence[idx]
    return sequence[idx] + mul * extrapolate(diffs, left=left)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {sum(extrapolate(seq) for seq in data)}")
    print(f"Part 2: {sum(extrapolate(seq, left=True) for seq in data)}")
