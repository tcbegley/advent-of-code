import sys
from collections import defaultdict


def extract(line):
    components = line.split(' ')
    inc_map = {'inc': 1, 'dec': -1}
    return (
        components[0],
        inc_map[components[1]] * int(components[2]),
        (components[4], components[5], int(components[6]))
    )


def comp(x, op, y):
    if op == '>':
        return x > y
    if op == '>=':
        return x >= y
    if op == '==':
        return x == y
    if op == '<':
        return x < y
    if op == '<=':
        return x <= y
    if op == '!=':
        return x != y
    return False


def update(register, lines):
    for line in lines:
        reg, op, y = line[2]
        if comp(register[reg], op, y):
            register[line[0]] += line[1]


def answer(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().strip().split('\n')
    lines = list(map(extract, lines))
    register = defaultdict(lambda: 0)
    update(register, lines)
    return max(register.values())


if __name__ == "__main__":
    print(answer(sys.argv[1]))
