import sys


class Node:
    def __init__(self, children, metadata):
        self.metadata = metadata
        self.children = children


def build_tree(numbers):
    n_children = numbers[0]
    n_metadata = numbers[1]
    numbers = numbers[2:]
    children = []
    for i in range(n_children):
        numbers, node = build_tree(numbers)
        children.append(node)
    node = Node(children=children, metadata=numbers[:n_metadata])
    return numbers[n_metadata:], node


def sum_metadata(node):
    total = sum(node.metadata)
    for child in node.children:
        total += sum_metadata(child)
    return total


def answer(path):
    with open(path) as f:
        numbers = [int(i) for i in f.read().strip().split(" ")]

    (numbers, tree) = build_tree(numbers)

    if numbers:
        raise RuntimeError("Something went wrong with tree parsing")

    return sum_metadata(tree)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
