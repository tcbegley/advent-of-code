import sys


def load_data(path):
    with open(path) as f:
        return [grid.split("\n") for grid in f.read().strip().split("\n\n")]


def transpose(grid):
    return list(zip(*grid))


def reflections(grid, smudges=0):
    for r in range(1, len(grid)):
        if (
            sum(
                col1 != col2
                for row1, row2 in zip(grid[r - 1 :: -1], grid[r:])
                for col1, col2 in zip(row1, row2)
            )
            == smudges
        ):
            return r
    return 0


def part_1(data):
    return sum(reflections(transpose(grid)) + 100 * reflections(grid) for grid in data)


def part_2(data):
    return sum(
        reflections(transpose(grid), smudges=1) + 100 * reflections(grid, smudges=1)
        for grid in data
    )


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
