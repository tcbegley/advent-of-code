import sys


def load_data(path):
    with open(path) as f:
        return f.read().strip().split("\n\n")


def part_1(groups):
    return sum(len(set(g.replace("\n", ""))) for g in groups)


def part_2(groups):
    return sum(len(set.intersection(*[set(a) for a in g.split("\n")])) for g in groups)


if __name__ == "__main__":
    groups = load_data(sys.argv[1])
    print(f"Part 1: {part_1(groups)}")
    print(f"Part 2: {part_2(groups)}")
