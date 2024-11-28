import re
import sys
from collections import Counter

CLAIM_PATTERN = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")


def load_data(path):
    with open(path) as f:
        return [
            (id_, int(x0), int(y0), int(x_len), int(y_len))
            for id_, x0, y0, x_len, y_len in CLAIM_PATTERN.findall(f.read())
        ]


def get_counts(claims):
    counts = Counter()

    for _, x0, y0, x_len, y_len in claims:
        for x in range(x0, x0 + x_len):
            for y in range(y0, y0 + y_len):
                counts[(x, y)] += 1

    return counts


def part_1(claims):
    counts = get_counts(claims)
    return sum(v > 1 for v in counts.values())


def part_2(claims):
    counts = get_counts(claims)

    for id_, x0, y0, x_len, y_len in claims:
        if all(
            counts[(x, y)] == 1
            for x in range(x0, x0 + x_len)
            for y in range(y0, y0 + y_len)
        ):
            return id_


if __name__ == "__main__":
    claims = load_data(sys.argv[1])
    print(f"Part 1: {part_1(claims)}")
    print(f"Part 2: {part_2(claims)}")
