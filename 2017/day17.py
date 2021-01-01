import sys


def load_data(path):
    with open(path) as f:
        return int(f.read().strip())


def part_1(skip):
    list_ = [0]
    pos = 0
    for i in range(2017):
        pos = (pos + skip) % (i + 1) + 1
        list_.insert(pos, i + 1)
    return list_[list_.index(2017) + 1]


def part_2(skip):
    pos, after_zero = 0, None

    for i in range(50_000_000):
        pos = (pos + skip) % (i + 1) + 1
        if pos == 1:
            after_zero = i + 1

    return after_zero


if __name__ == "__main__":
    skip = load_data(sys.argv[1])
    print(f"Part 1: {part_1(skip)}")
    print(f"Part 2: {part_2(skip)}")
