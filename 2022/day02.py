import sys


def load_data(path):
    with open(path) as f:
        return [tuple(row.split(" ")) for row in f.read().strip().split("\n")]


def part_1(data):
    scores = {
        ("A", "X"): 1 + 3,
        ("A", "Y"): 2 + 6,
        ("A", "Z"): 3 + 0,
        ("B", "X"): 1 + 0,
        ("B", "Y"): 2 + 3,
        ("B", "Z"): 3 + 6,
        ("C", "X"): 1 + 6,
        ("C", "Y"): 2 + 0,
        ("C", "Z"): 3 + 3,
    }
    return sum(scores[row] for row in data)


def part_2(data):
    scores = {
        ("A", "X"): 0 + 3,
        ("A", "Y"): 3 + 1,
        ("A", "Z"): 6 + 2,
        ("B", "X"): 0 + 1,
        ("B", "Y"): 3 + 2,
        ("B", "Z"): 6 + 3,
        ("C", "X"): 0 + 2,
        ("C", "Y"): 3 + 3,
        ("C", "Z"): 6 + 1,
    }
    return sum(scores[row] for row in data)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
