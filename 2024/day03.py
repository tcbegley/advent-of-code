import re
import sys

MUL_PATTERN = re.compile(r"mul\((\d+),(\d+)\)")
MUL_DO_DONT_PATTERN = re.compile(r"(mul\((\d+),(\d+)\)|do\(\)|don't\(\))")


def load_data(path):
    with open(path) as f:
        return f.read().strip()


def part_1(data):
    muls = MUL_PATTERN.findall(data)
    return sum(int(a) * int(b) for a, b in muls)


def part_2(data):
    total = 0
    do = True
    for cmd, a, b in MUL_DO_DONT_PATTERN.findall(data):
        if do and cmd.startswith("mul"):
            total += int(a) * int(b)
        elif cmd == "do()":
            do = True
        elif cmd == "don't()":
            do = False
    return total


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
