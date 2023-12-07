import sys
from collections import Counter


VALUE_MAP = {v: i for i, v in enumerate("23456789TJQKA")}


def load_data(path):
    with open(path) as f:
        rows = [row.split(" ") for row in f.read().strip().split("\n")]
    return [(hand, int(bid)) for hand, bid in rows]


def key(hand, value_map, joker=False):
    counts = Counter(hand).most_common()
    if joker:
        counts = [(card, count) for card, count in counts if card != "J"]
        if counts:
            counts[0] = (counts[0][0], counts[0][1] + hand.count("J"))
        else:
            counts = [("J", 5)]
    return tuple(count for _, count in counts) + tuple(
        value_map[value] for value in hand
    )


def winnings(data, joker=False):
    if joker:
        value_map = {**VALUE_MAP, "J": -1}
    else:
        value_map = VALUE_MAP
    return sum(
        rank * bid
        for rank, (_, bid) in enumerate(
            sorted(data, key=lambda row: key(row[0], value_map, joker=joker)),
            start=1,
        )
    )


def part_1(data):
    return winnings(data)


def part_2(data):
    return winnings(data, joker=True)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
