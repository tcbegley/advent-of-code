import sys


def load_data(path):
    with open(path) as f:
        return [int(i) for i in f.read().strip()]


def part_1(numbers):
    return sum(
        numbers[i - 1]
        for i in range(len(numbers))
        if numbers[i] == numbers[i - 1]
    )


def part_2(numbers):
    n = len(numbers)
    return sum(
        numbers[i]
        for i in range(len(numbers))
        if numbers[i] == numbers[(i + n // 2) % n]
    )


if __name__ == "__main__":
    numbers = load_data(sys.argv[1])
    print(f"Part 1: {part_1(numbers)}")
    print(f"Part 2: {part_2(numbers)}")
