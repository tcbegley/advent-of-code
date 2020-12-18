import sys
from functools import reduce


def load_data(path):
    with open(path) as f:
        return f.read().strip().split("\n")


def bracket_matcher(s):
    if s.count("(") != s.count(")"):
        raise ValueError("Brackets don't match...")

    start = s.index("(")
    count = 1
    for i, c in enumerate(s):
        if i <= start:
            continue
        if c == "(":
            count += 1
        elif c == ")":
            count -= 1
        if count == 0:
            end = i + 1
            break

    return start, end


def recursor(s, process_fn):
    if "(" in s:
        start, end = bracket_matcher(s)
        res = recursor(s[start + 1 : end - 1], process_fn)
        return recursor(s[:start] + str(res) + s[end:], process_fn)
    return process_fn(s)


def process(s):
    s = s.split(" ")
    res, i = s[0], 1
    while i < len(s) - 1:
        res = eval(f"{res}{s[i]}{s[i+1]}")
        i += 2

    return res


def process2(s):
    return reduce(lambda a, b: a * b, [eval(x) for x in s.split(" * ")])


def part_1(lines):
    return sum(recursor(line, process) for line in lines)


def part_2(lines):
    return sum(recursor(line, process2) for line in lines)


if __name__ == "__main__":
    lines = load_data(sys.argv[1])
    print(f"Part 1: {part_1(lines)}")
    print(f"Part 2: {part_2(lines)}")
