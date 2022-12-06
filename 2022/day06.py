import sys


def load_data(path):
    with open(path) as f:
        return f.read().strip()


def first_unique_n(data, n):
    for i in range(n, len(data)):
        if len(set(data[i - n : i])) == n:
            return i


def part_1(data):
    return first_unique_n(data, 4)


def part_2(data):
    return first_unique_n(data, 14)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
