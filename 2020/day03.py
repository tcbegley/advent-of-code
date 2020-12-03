import sys


def answer(path):
    with open(path) as f:
        map_ = [line.strip() for line in f.readlines()]

    count = 0
    n = len(map_[0])

    for i, row in enumerate(map_):
        if row[(3 * i) % n] == "#":
            count += 1

    return count


if __name__ == "__main__":
    print(answer(sys.argv[1]))
