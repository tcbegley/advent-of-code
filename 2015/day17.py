import sys
from collections import defaultdict
from functools import lru_cache


def load_data(path):
    with open(path) as f:
        return tuple(reversed(sorted(int(i) for i in f.read().strip().split("\n"))))


@lru_cache
def count(quantity, num, containers):
    combinations = defaultdict(lambda: 0)
    for i, container in enumerate(containers):
        if quantity > container:
            counts = count(quantity - container, num + 1, containers[i + 1 :])
            for k, v in counts.items():
                combinations[k] += v
        elif quantity == container:
            combinations[num + 1] += 1
    return combinations


def part_1(containers):
    return sum(count(150, 0, containers).values())


def part_2(containers):
    combinations = count(150, 0, containers)
    min_value = min(combinations)
    return combinations[min_value]


if __name__ == "__main__":
    containers = load_data(sys.argv[1])
    print(f"Part 1: {part_1(containers)}")
    print(f"Part 2: {part_2(containers)}")
