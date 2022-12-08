import sys

AVAILABLE_SPACE = 70_000_000
DESIRED_SPACE = 30_000_000


class Node:
    def __init__(self, parent=None):
        self.parent = parent
        self.children = {}
        self.size = 0


def load_data(path):
    with open(path) as f:
        commands = [row.split(" ") for row in f.read().strip().split("\n")]

    pwd = root = Node()

    for cmd in commands:
        match cmd:
            case ["$", "cd", "/"]:
                pwd = root
            case ["$", "cd", ".."]:
                pwd = pwd.parent
            case ["$", "cd", dir_]:
                pwd = pwd.children.setdefault(dir_, Node(pwd))
            case ["$", "ls"] | ["dir", _]:
                pass
            case [size, _]:
                node, size = pwd, int(size)
                while node is not None:
                    node.size += size
                    node = node.parent

    return root


def get_sizes(node):
    yield node.size
    for child in node.children.values():
        yield from get_sizes(child)


def part_1(root):
    return sum(size for size in get_sizes(root) if size <= 100_000)


def part_2(root):
    target_size = DESIRED_SPACE - (AVAILABLE_SPACE - root.size)
    return min(size for size in get_sizes(root) if size > target_size)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
