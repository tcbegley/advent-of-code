import re
import sys
from functools import reduce

NUMBER = re.compile(r"\d+")


def load_data(path):
    with open(path) as f:
        time, distance = f.read().strip().split("\n")
    time, distance = [int(n) for n in NUMBER.findall(time)], [
        int(n) for n in NUMBER.findall(distance)
    ]
    return time, distance


def bin_search(fn, low, high, left=True):
    result = None

    while low <= high:
        mid = (low + high) // 2
        if fn(mid) > 0:
            result = mid
            if left:
                high = mid - 1
            else:
                low = mid + 1
        else:
            if left:
                low = mid + 1
            else:
                high = mid - 1

    return result


def count(time, distance):
    def fn(button):
        return button * (time - button) - distance

    return (
        bin_search(fn, time // 2, time, left=False)
        - bin_search(fn, 0, time // 2, left=True)
        + 1
    )


def part_1(time, distance):
    return reduce(
        lambda a, b: a * b, (count(t, d) for t, d in zip(time, distance)), 1
    )


def part_2(time, distance):
    time = int("".join(map(str, time)))
    distance = int("".join(map(str, distance)))
    return count(time, distance)


if __name__ == "__main__":
    time, distance = load_data(sys.argv[1])
    print(f"Part 1: {part_1(time, distance)}")
    print(f"Part 2: {part_2(time, distance)}")
