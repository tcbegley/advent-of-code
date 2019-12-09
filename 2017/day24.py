import sys
from functools import reduce


def search(chain, unused):
    ms = sum(reduce(lambda x, y: x + y, chain, [0]))
    for i, comp in enumerate(unused):
        if not chain:
            if comp[0] == 0:
                ms = max(ms, search([comp], unused[:i] + unused[i + 1 :]))
            elif comp[1] == 0:
                ms = max(
                    ms,
                    search([[comp[1], comp[0]]], unused[:i] + unused[i + 1 :]),
                )
        else:
            if comp[0] == chain[-1][1]:
                ms = max(
                    ms, search(chain + [comp], unused[:i] + unused[i + 1 :])
                )
            if comp[1] == chain[-1][1]:
                ms = max(
                    ms,
                    search(
                        chain + [[comp[1], comp[0]]],
                        unused[:i] + unused[i + 1 :],
                    ),
                )
    return ms


def answer(file_path):
    with open(file_path, "r") as f:
        components = f.read().strip().split("\n")
    components = [list(map(int, c.split("/"))) for c in components]
    return search([], components)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
