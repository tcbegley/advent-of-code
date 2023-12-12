import sys
from collections import Counter
from functools import reduce


class Node:
    def __init__(self, name, val, children):
        self.name = name
        self.val = val
        self.children = children
        self.total = None


def load_data(path):
    with open(path) as f:
        return [extract(line.strip()) for line in f.readlines()]


def extract(line):
    line = line.split(" -> ")
    if len(line) > 1:
        children = line[1].split(", ")
    else:
        children = []
    parent, val = line[0].split(" ")
    val = int(val.strip("()"))
    return parent, val, children


def make_tree(node, val_lookup, child_lookup):
    return Node(
        node,
        val_lookup[node],
        [make_tree(child, val_lookup, child_lookup) for child in child_lookup[node]],
    )


def get_root(nodes):
    parents = set(node[0] for node in nodes)
    children = set(list(reduce(lambda x, y: x + y, [node[2] for node in nodes])))
    return next(iter(parents - children))


def gen_totals(node):
    if node.total is not None:
        return node.total
    node.total = sum(gen_totals(child) for child in node.children) + node.val
    return node.total


def search(tree):
    totals = [node.total for node in tree.children]
    if len(set(totals)) == 1:
        return "pass"
    counts = Counter(totals).most_common()
    node = tree.children[totals.index(counts[1][0])]
    val = search(node)
    if val == "pass":
        return node.val - counts[1][0] + counts[0][0]
    return val


def part_1(nodes):
    return get_root(nodes)


def part_2(nodes):
    val_lookup = {node[0]: node[1] for node in nodes}
    child_lookup = {node[0]: node[2] for node in nodes}
    tree = make_tree(get_root(nodes), val_lookup, child_lookup)
    gen_totals(tree)
    return search(tree)


if __name__ == "__main__":
    nodes = load_data(sys.argv[1])
    print(f"Part 1: {part_1(nodes)}")
    print(f"Part 2: {part_2(nodes)}")
