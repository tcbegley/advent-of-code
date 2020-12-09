import sys


def load_data(path):
    with open(path) as f:
        return [line.strip() for line in f.readlines()]


def count(right, down, map_):
    total = 0
    n = len(map_[0])

    for i in range(0, len(map_), down):
        if map_[i][(right * i // down) % n] == "#":
            total += 1

    return total


def part_1(map_):
    return count(3, 1, map_)


def part_2(map_):
    return (
        count(1, 1, map_)
        * count(3, 1, map_)
        * count(5, 1, map_)
        * count(7, 1, map_)
        * count(1, 2, map_)
    )


if __name__ == "__main__":
    map_ = load_data(sys.argv[1])
    print(f"Part 1: {part_1(map_)}")
    print(f"Part 2: {part_2(map_)}")
