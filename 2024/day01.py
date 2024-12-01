import sys
from collections import Counter


def load_data(path):
    with open(path) as f:
        return zip(
            *(map(int, row.split("   ")) for row in f.read().strip().split("\n"))
        )


def part_1(list1, list2):
    return sum(abs(b - a) for a, b in zip(sorted(list1), sorted(list2)))


def part_2(list1, list2):
    counts = Counter(list2)
    return sum(a * counts[a] for a in list1)


if __name__ == "__main__":
    list1, list2 = load_data(sys.argv[1])
    print(f"Part 1: {part_1(list1, list2)}")
    print(f"Part 2: {part_2(list1, list2)}")
