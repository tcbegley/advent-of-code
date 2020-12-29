import sys
from collections import defaultdict


def load_data(path):
    with open(path) as f:
        return [extract(line) for line in f.readlines()]


def extract(line):
    components = line.strip().split(" ")
    inc_map = {"inc": 1, "dec": -1}
    return (
        components[0],
        inc_map[components[1]] * int(components[2]),
        (components[4], components[5], int(components[6])),
    )


def comp(x, op, y):
    if op == ">":
        return x > y
    if op == ">=":
        return x >= y
    if op == "==":
        return x == y
    if op == "<":
        return x < y
    if op == "<=":
        return x <= y
    if op == "!=":
        return x != y
    return False


def update(register, lines):
    max_val = 0
    for line in lines:
        reg, op, y = line[2]
        if comp(register[reg], op, y):
            register[line[0]] += line[1]
        cur_max = max(register.values())
        max_val = max(max_val, cur_max)
    return max_val


def part_1(instructions):
    register = defaultdict(lambda: 0)
    update(register, instructions)
    return max(register.values())


def part_2(instructions):
    register = defaultdict(lambda: 0)
    return update(register, instructions)


if __name__ == "__main__":
    instructions = load_data(sys.argv[1])
    print(f"Part 1: {part_1(instructions)}")
    print(f"Part 2: {part_2(instructions)}")
