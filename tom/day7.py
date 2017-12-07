import sys
from functools import reduce


def extract(line):
    line = line.split(' -> ')
    if len(line) > 1:
        children = line[1].split(', ')
    else:
        children = []
    parent, val = line[0].split(' ')
    val = int(val[1: -1])
    return parent, val, children


def get_root(lines):
    nodes = set([line[0] for line in lines])
    children = set(reduce(lambda x, y: x+y, [line[2] for line in lines]))
    return list(nodes - children)[0]


def answer(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().strip().split('\n')
    lines = list(map(extract, lines))
    return get_root(lines)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
