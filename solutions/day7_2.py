import sys
from collections import Counter
from functools import reduce


class Node:
    def __init__(self, name, val, children):
        self.name = name
        self.val = val
        self.children = children
        self.total = None


def extract(line):
    line = line.split(' -> ')
    if len(line) > 1:
        children = line[1].split(', ')
    else:
        children = []
    parent, val = line[0].split(' ')
    val = int(val[1: -1])
    return parent, val, children


def make_tree(node, val_lookup, child_lookup):
    return Node(node, val_lookup[node],
                [make_tree(child, val_lookup, child_lookup)
                 for child in child_lookup[node]])


def get_root(lines):
    nodes = set([line[0] for line in lines])
    children = set(reduce(lambda x, y: x+y, [line[2] for line in lines]))
    return list(nodes - children)[0]


def gen_totals(node):
    if node.total is not None:
        return node.total
    node.total = sum(gen_totals(child) for child in node.children) + node.val
    return node.total


def search(tree):
    totals = [node.total for node in tree.children]
    if len(set(totals)) == 1:
        return 'pass'
    counts = Counter(totals).most_common()
    node = tree.children[totals.index(counts[1][0])]
    val = search(node)
    if val == 'pass':
        return node.val - counts[1][0] + counts[0][0]
    return val


def answer(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().strip().split('\n')
    lines = list(map(extract, lines))
    val_lookup = dict((line[0], line[1]) for line in lines)
    child_lookup = dict((line[0], line[2]) for line in lines)
    tree = make_tree(get_root(lines), val_lookup, child_lookup)
    gen_totals(tree)
    return search(tree)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
