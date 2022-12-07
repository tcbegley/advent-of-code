import sys

AVAILABLE_SPACE = 70_000_000
DESIRED_SPACE = 30_000_000


class Node:
    def __init__(self, parent=None):
        self.parent = parent
        self.children = {}
        self.files = {}


def load_data(path):
    with open(path) as f:
        data = [row.split(" ") for row in f.read().strip().split("\n")]

    root = Node()
    pwd = root

    for row in data:
        if row[0] == "$":
            if row[1] == "cd":
                if row[2] == "..":
                    pwd = pwd.parent
                elif row[2] == "/":
                    pwd = root
                else:
                    pwd = pwd.children[row[2]]
        else:
            if row[0] == "dir":
                if row[1] not in pwd.children:
                    pwd.children[row[1]] = Node(pwd)
            else:
                pwd.files[row[1]] = int(row[0])

    return root


def part_1(root):
    total = 0

    def get_total_size(node):
        total_size = sum(node.files.values()) + sum(
            get_total_size(child) for child in node.children.values()
        )
        if total_size <= 100_000:
            nonlocal total
            total += total_size
        return total_size

    get_total_size(root)

    return total


def part_2(root):
    total = []

    def get_total_size(node):
        total_size = sum(node.files.values()) + sum(
            get_total_size(child) for child in node.children.values()
        )
        nonlocal total
        total.append(total_size)
        return total_size

    target_size = DESIRED_SPACE - (AVAILABLE_SPACE - get_total_size(root))

    return min(t for t in total if t > target_size)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
