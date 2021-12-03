import sys


def load_numbers(path):
    with open(path) as f:
        numbers = [line.strip() for line in f.readlines()]
    num_digits = len(numbers[0])
    return [int(num, base=2) for num in numbers], num_digits


def part_1(numbers, num_digits):
    gamma = sum(
        1 << i
        for i in range(num_digits - 1, -1, -1)
        if 2 * sum((num >> i) & 1 for num in numbers) >= len(numbers)
    )
    epsilon = ~gamma & ((1 << num_digits) - 1)
    return gamma * epsilon


def count_ones(numbers, position):
    return sum((num >> position) & 1 for num in numbers)


def filter_numbers(numbers, num_digits, most_common=True):
    i = num_digits - 1

    while len(numbers) > 1:
        ones = count_ones(numbers, i)
        if most_common ^ (ones < len(numbers) - ones):
            numbers = [num for num in numbers if num & 1 << i]
        else:
            numbers = [num for num in numbers if not num & 1 << i]
        i -= 1

    return numbers[0]


def part_2(numbers, num_digits):
    return filter_numbers(numbers, num_digits) * filter_numbers(
        numbers, num_digits, most_common=False
    )


if __name__ == "__main__":
    numbers, num_digits = load_numbers(sys.argv[1])
    print(f"Part 1: {part_1(numbers, num_digits)}")
    print(f"Part 2: {part_2(numbers, num_digits)}")
