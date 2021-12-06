import sys
from collections import Counter


def load_data(path):
    with open(path) as f:
        return [int(n) for n in f.read().strip().split(",")]


def answer(data, n_periods=80):
    fish = dict(Counter(data))

    for _ in range(n_periods):
        new_fish = {}
        for days, count in fish.items():
            if days > 0:
                new_fish[days - 1] = count
        new_fish[6] = new_fish.get(6, 0) + fish.get(0, 0)
        new_fish[8] = fish.get(0, 0)
        fish = new_fish

    return sum(fish.values())


def part_1(data):
    return answer(data, n_periods=80)


def part_2(data):
    return answer(data, n_periods=256)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
