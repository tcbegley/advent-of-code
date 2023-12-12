import sys
from itertools import product


def load_data(path):
    with open(path) as f:
        algorithm, image = f.read().strip().split("\n\n")

    algorithm = [1 if c == "#" else 0 for c in algorithm]
    lit = {
        (i, j)
        for i, row in enumerate(image.split("\n"))
        for j, c in enumerate(row)
        if c == "#"
    }
    unlit = {
        (i, j)
        for i, row in enumerate(image.split("\n"))
        for j, c in enumerate(row)
        if c == "."
    }
    return algorithm, lit, unlit


def patch_to_index(lit, unlit, x, y, default=False):
    locs = product((1, 0, -1), (1, 0, -1))

    if default:
        return sum(
            1 << i for i, (dx, dy) in enumerate(locs) if (x + dx, y + dy) not in unlit
        )
    return sum(1 << i for i, (dx, dy) in enumerate(locs) if (x + dx, y + dy) in lit)


def get_all_neighbours(lit, unlit):
    merged = lit | unlit
    x_min, x_max = min(x for x, _ in merged), max(x for x, _ in merged)
    y_min, y_max = min(y for _, y in merged), max(y for _, y in merged)
    return product(range(x_min - 1, x_max + 2), range(y_min - 1, y_max + 2))


def update(algorithm, lit, unlit, default=False):
    new_lit, new_unlit = set(), set()

    for x, y in get_all_neighbours(lit, unlit):
        if algorithm[patch_to_index(lit, unlit, x, y, default)] == 1:
            new_lit.add((x, y))
        else:
            new_unlit.add((x, y))

    if default:
        default = algorithm[-1] == 1
    else:
        default = algorithm[0] == 1

    return new_lit, new_unlit, default


def answer(algorithm, lit, unlit, n=2):
    default = False
    for _ in range(n):
        lit, unlit, default = update(algorithm, lit, unlit, default)

    return len(lit)


def part_1(algorithm, lit, unlit):
    return answer(algorithm, lit, unlit)


def part_2(algorithm, lit, unlit):
    return answer(algorithm, lit, unlit, n=50)


if __name__ == "__main__":
    algorithm, lit, unlit = load_data(sys.argv[1])
    print(f"Part 1: {part_1(algorithm, lit, unlit)}")
    print(f"Part 2: {part_2(algorithm, lit, unlit)}")
