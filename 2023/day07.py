import sys
from collections import Counter


VALUE_MAP = {v: i for i, v in enumerate("23456789TJQKA")}


def load_data(path):
    with open(path) as f:
        rows = [row.split(" ") for row in f.read().strip().split("\n")]
    return [(hand, int(bid)) for hand, bid in rows]


def key(hand):
    counts = Counter(hand).most_common()
    return tuple(count for _, count in counts) + tuple(
        VALUE_MAP[value] for value in hand
    )


def part_1(data):
    return sum(
        rank * bid
        for rank, (_, bid) in enumerate(
            sorted(data, key=lambda row: key(row[0])), start=1
        )
    )


def part_2(data):
    pass


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
