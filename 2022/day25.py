import sys
from math import log

DIGITS = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
REVERSE_DIGITS = "=-012"


def load_data(path):
    with open(path) as f:
        return f.read().strip().split("\n")


def snafu_to_decimal(s):
    factor = 1
    out = 0
    for c in s[::-1]:
        out += DIGITS[c] * factor
        factor *= 5
    return out


def decimal_to_quinary(n):
    out = []
    while n:
        out.append(n % 5)
        n //= 5
    return [x for x in reversed(out)]


def twos(n):
    # computes the value of 2222 (n times) in base 5
    factor = 1
    out = 0
    for _ in range(n):
        out += 2 * factor
        factor *= 5
    return out


def decimal_to_snafu(n):
    n_digits = round(log(n, 5)) + 1
    offset = twos(n_digits)
    digits = decimal_to_quinary(n + offset)
    return "".join([REVERSE_DIGITS[d] for d in digits]).lstrip("0")


def part_1(data):
    return decimal_to_snafu(sum(snafu_to_decimal(s) for s in data))


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
