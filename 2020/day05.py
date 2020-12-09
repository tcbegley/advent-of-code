import sys


def load_data(path):
    trans_table = str.maketrans({"R": "1", "B": "1", "F": "0", "L": "0"})
    with open(path) as f:
        return [
            int(p, 2)
            for p in f.read().strip().translate(trans_table).split("\n")
        ]


def part_1(passes):
    return max(passes)


def part_2(passes):
    return next(iter(set(range(min(passes), max(passes) + 1)) - set(passes)))


if __name__ == "__main__":
    passes = load_data(sys.argv[1])
    print(f"Part 1: {part_1(passes)}")
    print(f"Part 2: {part_2(passes)}")
