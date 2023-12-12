import sys


def load_data(path):
    with open(path) as f:
        return [
            [[int(id_) for id_ in pair.split("-")] for pair in row.split(",")]
            for row in f.read().strip().split("\n")
        ]


def part_1(data):
    count = 0
    for (low1, high1), (low2, high2) in data:
        if (low1 <= low2 and high2 <= high1) or (low2 <= low1 and high1 <= high2):
            count += 1
    return count


def part_2(data):
    count = 0
    for (low1, high1), (low2, high2) in data:
        if low1 <= low2 <= high1 or low2 <= low1 <= high2:
            count += 1
    return count


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
