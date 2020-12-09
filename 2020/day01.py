import sys


def load_data(path):
    with open(path) as f:
        return set(int(n) for n in f.read().strip().split("\n"))


def part_1(numbers):
    for i in numbers:
        if (j := 2020 - i) in numbers:
            return i * j


def part_2(numbers):
    for i in numbers:
        for j in numbers:
            if (k := 2020 - i - j) in numbers:
                return i * j * k


if __name__ == "__main__":
    numbers = load_data(sys.argv[1])
    print(f"Part 1: {part_1(numbers)}")
    print(f"Part 2: {part_2(numbers)}")
