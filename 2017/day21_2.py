import sys

import numpy as np


def to_array(string):
    return np.array([[c for c in s] for s in string.split("/")])


def to_string(arr):
    return "/".join("".join(map(str, row)) for row in arr)


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


def answer(file_path):
    with open(file_path, "r") as f:
        lookup = dict(
            line.split(" => ") for line in f.read().strip().split("\n")
        )
    permute(lookup)
    fractal = ".#./..#/###"
    for i in range(18):
        fractal = to_array(fractal)
        size = len(fractal)
        if size % 2 == 0:
            blocks = [
                [
                    to_string(fractal[i : i + 2, j : j + 2])
                    for j in range(0, size, 2)
                ]
                for i in range(0, size, 2)
            ]
        else:
            blocks = [
                [
                    to_string(fractal[i : i + 3, j : j + 3])
                    for j in range(0, size, 3)
                ]
                for i in range(0, size, 3)
            ]
        blocks = [[to_array(lookup[s]) for s in row] for row in blocks]
        fractal = to_string(
            np.concatenate([np.concatenate(row, axis=1) for row in blocks])
        )
    return fractal.count("#")


if __name__ == "__main__":
    print(answer(sys.argv[1]))
