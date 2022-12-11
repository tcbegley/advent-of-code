import sys


class Node:
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata


def load_data(path):
    with open(path) as f:
        data = map(int, f.read().strip().split(" "))

    root, data = parse_node(data)
    if data:
        raise RuntimeError("Error parsing data")

    return root


def parse_node(data):
    n_children, n_metadata, *data = data
    children = []
    for _ in range(n_children):
        node, data = parse_node(data)
        children.append(node)
    return Node(children, data[:n_metadata]), data[n_metadata:]


def sum_metadata(node):
    return sum(node.metadata) + sum(
        sum_metadata(child) for child in node.children
    )


def part_1(root):
    return sum_metadata(root)


def value(node):
    if node.children:
        return sum(
            value(node.children[i - 1])
            for i in node.metadata
            if 1 <= i <= len(node.children)
        )
    return sum(node.metadata)


def part_2(root):
    return value(root)


if __name__ == "__main__":
    root = load_data(sys.argv[1])
    print(f"Part 1: {part_1(root)}")
    print(f"Part 2: {part_2(root)}")
