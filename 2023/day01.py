import sys
from string import digits

NUMBERS = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def load_data(path):
    with open(path) as f:
        return f.read().strip().split("\n")


def find_all(s, targets):
    # do this instead of regex to make sure we find overlapping examples
    i = 0
    while i < len(s):
        for target in targets:
            if s[i:].startswith(target):
                yield target
                break
        i += 1


def calibration_value(s, lookup):
    numbers = [lookup[num] for num in find_all(s, lookup)]
    return int(numbers[0] + numbers[-1])


def solve(data, lookup):
    return sum(calibration_value(d, lookup) for d in data)


if __name__ == "__main__":
    data = load_data(sys.argv[1])

    lookup1 = {d: str(i) for i, d in enumerate(digits)}
    lookup2 = {**lookup1, **{num: str(i) for i, num in enumerate(NUMBERS)}}
    print(f"Part 1: {solve(data, lookup1)}")
    print(f"Part 2: {solve(data, lookup2)}")
