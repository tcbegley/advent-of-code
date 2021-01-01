import sys
from itertools import chain


def load_data(path):
    with open(path) as f:
        return dict(
            line.split(" => ") for line in f.read().strip().split("\n")
        )


def to_array(string):
    return [[c for c in s] for s in string.split("/")]


def to_string(arr):
    return "/".join("".join(map(str, row)) for row in arr)


def concatenate_blocks(blocks):
    return list(
        chain(
            *[[list(chain(*rows)) for rows in zip(*block)] for block in blocks]
        )
    )


def gen_flips(k):
    perms = []
    k = [[c for c in r] for r in k.split("/")]
    perms.append([list(reversed(r)) for r in k])
    perms.append(list(reversed(k)))
    return ["/".join(["".join(r) for r in perm]) for perm in perms]


def gen_rots(k):
    perms = []
    k = [[c for c in r] for r in k.split("/")]
    perms.append(
        [[k[len(k) - j - 1][i] for j in range(len(k))] for i in range(len(k))]
    )
    perms.append(list(reversed([list(reversed(r)) for r in k])))
    perms.append(
        [[k[j][len(k) - i - 1] for j in range(len(k))] for i in range(len(k))]
    )
    return ["/".join(["".join(r) for r in perm]) for perm in perms]


def permute(lookup):
    new = []
    for k, v in lookup.items():
        for new_key in gen_flips(k):
            new.append((new_key, v))
    lookup.update(new)
    new = []
    for k, v in lookup.items():
        for new_key in gen_rots(k):
            new.append((new_key, v))
    lookup.update(new)


def iterate(lookup, iterations):
    permute(lookup)
    fractal = ".#./..#/###"
    for i in range(iterations):
        fractal = to_array(fractal)
        size = len(fractal)
        if size % 2 == 0:
            blocks = [
                [
                    to_string(
                        [
                            [fractal[row][col] for col in range(j, j + 2)]
                            for row in range(i, i + 2)
                        ]
                    )
                    for j in range(0, size, 2)
                ]
                for i in range(0, size, 2)
            ]
        else:
            blocks = [
                [
                    to_string(
                        [
                            [fractal[row][col] for col in range(j, j + 3)]
                            for row in range(i, i + 3)
                        ]
                    )
                    for j in range(0, size, 3)
                ]
                for i in range(0, size, 3)
            ]
        blocks = [[to_array(lookup[s]) for s in row] for row in blocks]
        fractal = to_string(concatenate_blocks(blocks))
    return fractal.count("#")


def part_1(lookup):
    return iterate(lookup, 5)


def part_2(lookup):
    return iterate(lookup, 18)


if __name__ == "__main__":
    lookup = load_data(sys.argv[1])
    print(f"Part 1: {part_1(lookup)}")
    print(f"Part 2: {part_2(lookup)}")
