import sys


def load_data(path):
    with open(path) as f:
        return f.read().strip()


def part_1(directions):
    return directions.count("(") - directions.count(")")


def part_2(directions):
    floor = 0
    for i, direction in enumerate(directions, start=1):
        if direction == "(":
            floor += 1
        else:
            floor -= 1
        if floor < 0:
            return i
    return None


if __name__ == "__main__":
    directions = load_data(sys.argv[1])
    print(f"Part 1: {part_1(directions)}")
    print(f"Part 2: {part_2(directions)}")
