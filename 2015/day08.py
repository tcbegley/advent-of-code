import re
import sys

ESCAPED = re.compile(r"\\\\|\\\"")
HEX = re.compile(r"\\x[0-9a-f]{2}")


def load_data(path):
    with open(path) as f:
        return f.read().strip().split("\n")


def part_1(strings):
    return sum(
        2 + len(ESCAPED.findall(s)) + 3 * len(HEX.findall(s)) for s in strings
    )


def part_2(strings):
    return sum(2 + s.count('"') + s.count("\\") for s in strings)


if __name__ == "__main__":
    strings = load_data(sys.argv[1])
    print(f"Part 1: {part_1(strings)}")
    print(f"Part 2: {part_2(strings)}")
