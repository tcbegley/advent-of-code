import sys
from collections import defaultdict


def load_data(path):
    def process_line(line):
        return tuple(map(int, line.strip().split("-")))

    with open(path) as f:
        return [process_line(line) for line in f.readlines()]


def part_1(blacklist):
    blacklist = sorted(blacklist)

    min_allowed = 0
    for low, high in blacklist:
        if min_allowed >= low:
            min_allowed = max(min_allowed, high + 1)
        else:
            break

    return min_allowed


def part_2(blacklist):
    # iteratively build up the terms in this formula:
    # https://proofwiki.org/wiki/Cardinality_of_Set_Union#General_Case
    counts = defaultdict(int)
    for low1, high1 in blacklist:
        for (low2, high2), count in list(counts.items()):
            low = max(low1, low2)
            high = min(high1, high2)
            if low <= high:
                counts[(low, high)] -= count
        counts[(low1, high1)] += 1

    return 2**32 - sum(
        (high - low + 1) * count for (low, high), count in counts.items()
    )


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
