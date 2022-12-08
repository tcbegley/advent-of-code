import sys
from functools import reduce


def load_data(path):
    with open(path) as f:
        return [list(map(int, row)) for row in f.read().strip().split("\n")]


def mark_visible(trees, visible, coordinate_map):
    max_height = float("-inf")

    for i, tree in enumerate(trees):
        if tree > max_height:
            visible.add(coordinate_map(i))
            max_height = tree


def part_1(trees):
    visible = set()

    for r, row in enumerate(trees):
        mark_visible(row, visible, lambda c: (r, c))
        mark_visible(row[::-1], visible, lambda c: (r, len(row) - 1 - c))

    for c, col in enumerate(zip(*trees)):
        mark_visible(col, visible, lambda r: (r, c))
        mark_visible(col[::-1], visible, lambda r: (len(trees) - 1 - r, c))

    return len(visible)


def count_shorter(trees, r, c, dr, dc):
    max_x, max_y = len(trees), len(trees[0])
    height = trees[r][c]
    count = 0
    r, c = r + dr, c + dc

    while 0 <= r < max_x and 0 <= c < max_y:
        count += 1
        if trees[r][c] >= height:
            break
        r, c = r + dr, c + dc

    return count


def scenic_score(trees, r, c):
    scores = [
        count_shorter(trees, r, c, dr, dc)
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
    ]
    return reduce(lambda a, b: a * b, scores, 1)


def part_2(trees):
    return max(
        scenic_score(trees, r, c)
        for r in range(len(trees))
        for c in range(len(trees[0]))
    )


if __name__ == "__main__":
    trees = load_data(sys.argv[1])
    print(f"Part 1: {part_1(trees)}")
    print(f"Part 2: {part_2(trees)}")
