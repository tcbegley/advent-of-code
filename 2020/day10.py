import sys
from functools import lru_cache


@lru_cache
def fib3(n):
    if n <= 1:
        return 1
    elif n == 2:
        return 2
    elif n == 3:
        return 4
    return fib3(n - 1) + fib3(n - 2) + fib3(n - 3)


def load_data(path):
    with open(path) as f:
        numbers = [0] + sorted(int(n) for n in f.read().strip().split("\n"))

    return [x - y for x, y in zip(numbers[1:], numbers[:-1])]


def part_1(diffs):
    return diffs.count(1) * (diffs.count(3) + 1)


def part_2(diffs):
    n = len(diffs)
    count = 1
    left = 0

    while left < n:
        if diffs[left] == 3:
            left += 1
        else:
            right = left + 1
            while right < n and diffs[right] == 1:
                right += 1
            count *= fib3(right - left)
            left = right

    return count


if __name__ == "__main__":
    diffs = load_data(sys.argv[1])
    print(f"Part 1: {part_1(diffs)}")
    print(f"Part 2: {part_2(diffs)}")  # can't drop first or last
