import sys


def parse_lock(s):
    return [sum(s[5 * i + j] == "#" for i in range(1, 6)) for j in range(5)]


def load_data(path):
    with open(path) as f:
        blocks = f.read().strip().split("\n\n")

    locks = []
    keys = []

    for block in blocks:
        if block[0] == "#":
            locks.append(parse_lock(block.replace("\n", "")))
        else:
            keys.append(
                [
                    height
                    for height in reversed(parse_lock(block[::-1].replace("\n", "")))
                ]
            )

    return locks, keys


def compatible(lock, key):
    return all(l_height + k_height <= 5 for l_height, k_height in zip(lock, key))


def part_1(locks, keys):
    return sum(compatible(lock, key) for lock in locks for key in keys)


if __name__ == "__main__":
    locks, keys = load_data(sys.argv[1])
    print(f"Part 1: {part_1(locks, keys)}")
