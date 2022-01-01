import re
import sys

NUMBER = re.compile(r"\d+")


def load_data(path):
    with open(path) as f:
        lines = f.readlines()

    x, y = NUMBER.findall(lines[1] + lines[2])
    return int(x), int(y)


def alternating_bits(num_bits):
    # find the integer whose binary representation is num_bits alternating bits
    return sum(1 << i for i in range(1, num_bits, 2))


def part_1(x, y):
    # program cycles through the binary representation of a + x * y
    # so we find the smallest number greater than x * y with alternating bits
    # and subtract x * y to find a
    offset = x * y
    num_bits = offset.bit_length()
    if alternating_bits(num_bits) >= offset:
        return alternating_bits(num_bits) - offset
    return alternating_bits(num_bits + 2) - offset


if __name__ == "__main__":
    x, y = load_data(sys.argv[1])
    print(f"Part 1: {part_1(x, y)}")
