import sys


def load_data(path):
    with open(path) as f:
        ranges, ids = f.read().strip().split("\n\n")

    ranges = [list(map(int, row.split("-"))) for row in ranges.split("\n")]
    ids = [int(id_) for id_ in ids.split("\n")]

    return ranges, ids


def part_1(ranges, ids):
    return sum(any(low <= id_ <= high for low, high in ranges) for id_ in ids)


def merge_ranges(ranges):
    ranges = sorted(ranges)
    merged = []

    for r in ranges:
        if merged and merged[-1][1] >= r[0]:
            merged[-1][1] = max(merged[-1][1], r[1])
        else:
            merged.append(r)

    return merged


def part_2(ranges):
    ranges = merge_ranges(ranges)
    return sum(high - low + 1 for low, high in ranges)


if __name__ == "__main__":
    ranges, ids = load_data(sys.argv[1])
    print(f"Part 1: {part_1(ranges, ids)}")
    print(f"Part 2: {part_2(ranges)}")
