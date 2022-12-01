import sys


def load_data(path):
    with open(path) as f:
        return [
            sum(int(row) for row in block.split("\n"))
            for block in f.read().strip().split("\n\n")
        ]


def part_1(calorie_counts):
    return max(calorie_counts)


def part_2(calorie_counts):
    return sum(sorted(calorie_counts, reverse=True)[:3])


if __name__ == "__main__":
    calorie_counts = load_data(sys.argv[1])
    print(f"Part 1: {part_1(calorie_counts)}")
    print(f"Part 2: {part_2(calorie_counts)}")
