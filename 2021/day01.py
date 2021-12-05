import sys


def load_data(path):
    with open(path) as f:
        return [int(n) for n in f.read().strip().split("\n")]


def answer(depths, offset=1):
    return sum(d2 > d1 for d2, d1 in zip(depths[offset:], depths))


def part_1(depths):
    return answer(depths)


def part_2(depths):
    return answer(depths, offset=3)


if __name__ == "__main__":
    depths = load_data(sys.argv[1])
    print(f"Part 1: {part_1(depths)}")
    print(f"Part 2: {part_2(depths)}")
