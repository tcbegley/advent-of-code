import hashlib
import sys


def load_data(path):
    with open(path) as f:
        return f.read().strip()


def mine(key, leading_zeros):
    prefix = "0" * leading_zeros
    i = 0
    while True:
        hash_ = hashlib.md5(f"{key}{i}".encode())
        if hash_.hexdigest().startswith(prefix):
            break
        i += 1
    return i


def part_1(key):
    return mine(key, 5)


def part_2(key):
    return mine(key, 6)


if __name__ == "__main__":
    key = load_data(sys.argv[1])
    print(f"Part 1: {part_1(key)}")
    print(f"Part 2: {part_2(key)}")
