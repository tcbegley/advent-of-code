import sys


def count(right, down, map_):
    total = 0
    n = len(map_[0])

    for i in range(0, len(map_), down):
        if map_[i][(right * i // down) % n] == "#":
            total += 1

    return total


def answer(path):
    with open(path) as f:
        map_ = [line.strip() for line in f.readlines()]

    return (
        count(1, 1, map_)
        * count(3, 1, map_)
        * count(5, 1, map_)
        * count(7, 1, map_)
        * count(1, 2, map_)
    )


if __name__ == "__main__":
    print(answer(sys.argv[1]))
