import sys
from functools import reduce


def search(chain, unused, ml, ms):
    if len(chain) > ml:
        ml = len(chain)
        ms = sum(reduce(lambda x, y: x + y, chain, [0]))
    elif len(chain) == ml:
        ms = max(ms, sum(reduce(lambda x, y: x + y, chain, [0])))
    for i, comp in enumerate(unused):
        if not chain:
            if comp[0] == 0:
                ml, ms = search([comp], unused[:i] + unused[i + 1 :], ml, ms)
            elif comp[1] == 0:
                ml, ms = search(
                    [[comp[1], comp[0]]], unused[:i] + unused[i + 1 :], ml, ms
                )
        else:
            if comp[0] == chain[-1][1]:
                ml, ms = search(
                    chain + [comp], unused[:i] + unused[i + 1 :], ml, ms
                )
            if comp[1] == chain[-1][1]:
                ml, ms = search(
                    chain + [[comp[1], comp[0]]],
                    unused[:i] + unused[i + 1 :],
                    ml,
                    ms,
                )
    return ml, ms


def answer(file_path):
    with open(file_path, "r") as f:
        components = f.read().strip().split("\n")
    components = [list(map(int, c.split("/"))) for c in components]
    return search([], components, 0, 0)[1]


if __name__ == "__main__":
    print(answer(sys.argv[1]))
