import sys


def load_data(path):
    with open(path) as f:
        return f.read().strip().split("\n")


def count_xmas(data, offsets):
    return sum(
        [data[r + r_off][c + c_off] for r_off, c_off in zip(*offsets)]
        in (["X", "M", "A", "S"], ["S", "A", "M", "X"])
        for r in range(len(data) - max(offsets[0]))
        for c in range(len(data[0]) - max(offsets[1]))
    )


def part_1(data):
    return sum(
        count_xmas(data, offsets)
        for offsets in [
            ((0, 0, 0, 0), (0, 1, 2, 3)),  # horizontal
            ((0, 1, 2, 3), (0, 0, 0, 0)),  # vertical
            ((0, 1, 2, 3), (0, 1, 2, 3)),  # major diagonal
            ((0, 1, 2, 3), (3, 2, 1, 0)),  # minor diagonal
        ]
    )


def part_2(data):
    return sum(
        # middle of the X is always A
        data[r][c] == "A"
        # the diagonally opposite characters should be different
        and data[r - 1][c - 1] != data[r + 1][c + 1]
        # there should be two Ms and two Ss
        and sorted(data[r + i][c + j] for i in [1, -1] for j in [1, -1])
        == ["M", "M", "S", "S"]
        for r in range(1, len(data) - 1)
        for c in range(1, len(data[0]) - 1)
    )


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
