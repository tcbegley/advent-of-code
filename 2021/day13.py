import sys


def load_data(path):
    def parse_dot(line):
        x, y = line.strip().split(",")
        return int(x), int(y)

    def parse_fold(line):
        _, line = line.strip().rsplit(" ", 1)
        axis, loc = line.split("=")
        return axis, int(loc)

    with open(path) as f:
        dots, folds = f.read().strip().split("\n\n")

    return {parse_dot(line) for line in dots.split("\n")}, [
        parse_fold(line) for line in folds.split("\n")
    ]


def fold(axis, loc, dots):
    if axis == "x":
        return {(x, y) if x < loc else (2 * loc - x, y) for x, y in dots}
    return {(x, y) if y < loc else (x, 2 * loc - y) for x, y in dots}


def part_1(dots, folds):
    axis, loc = folds[0]
    dots = fold(axis, loc, dots)
    return len(dots)


def part_2(dots, folds):
    for axis, loc in folds:
        dots = fold(axis, loc, dots)

    maxx = max(x for x, _ in dots)
    maxy = max(y for _, y in dots)

    solution_string = "\n".join(
        "".join("#" if (x, y) in dots else "." for x in range(maxx + 1))
        for y in range(maxy + 1)
    )
    return "\n" + solution_string


if __name__ == "__main__":
    dots, folds = load_data(sys.argv[1])
    print(f"Part 1: {part_1(dots, folds)}")
    print(f"Part 2: {part_2(dots, folds)}")
