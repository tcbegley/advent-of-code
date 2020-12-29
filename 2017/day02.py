import sys


def load_data(path):
    with open(path) as f:
        return [[int(i) for i in x.strip().split("\t")] for x in f.readlines()]


def divide(row):
    for i in range(len(row)):
        for j in range(len(row)):
            if i == j:
                continue
            if row[i] % row[j] == 0:
                return row[i] // row[j]
    return None


def part_1(numbers):
    return sum(max(row) - min(row) for row in numbers)


def part_2(numbers):
    return sum(divide(n) for n in numbers)


if __name__ == "__main__":
    numbers = load_data(sys.argv[1])
    print(f"Part 1: {part_1(numbers)}")
    print(f"Part 2: {part_2(numbers)}")
