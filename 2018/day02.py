import sys
from collections import defaultdict


def letter_counts(code):
    counts = defaultdict(lambda: 0)
    for c in code:
        counts[c] += 1
    return dict(counts)


def answer(path):
    with open(path) as f:
        codes = f.read().strip().split("\n")
    n2, n3 = 0, 0

    for code in codes:
        counts = letter_counts(code)
        values = set(counts.values())
        if 2 in values:
            n2 += 1
        if 3 in values:
            n3 += 1
    return n2 * n3


if __name__ == "__main__":
    print(answer(sys.argv[1]))
