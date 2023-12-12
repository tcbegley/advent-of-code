import sys
from functools import reduce


def load_data(path):
    with open(path) as f:
        return f.read().strip().split("\n")


def search1(chain, unused):
    ms = sum(reduce(lambda x, y: x + y, chain, [0]))
    for i, comp in enumerate(unused):
        if not chain:
            if comp[0] == 0:
                ms = max(ms, search1([comp], unused[:i] + unused[i + 1 :]))
            elif comp[1] == 0:
                ms = max(
                    ms,
                    search1([[comp[1], comp[0]]], unused[:i] + unused[i + 1 :]),
                )
        else:
            if comp[0] == chain[-1][1]:
                ms = max(ms, search1(chain + [comp], unused[:i] + unused[i + 1 :]))
            if comp[1] == chain[-1][1]:
                ms = max(
                    ms,
                    search1(
                        chain + [[comp[1], comp[0]]],
                        unused[:i] + unused[i + 1 :],
                    ),
                )
    return ms


def search2(chain, unused, ml, ms):
    if len(chain) > ml:
        ml = len(chain)
        ms = sum(reduce(lambda x, y: x + y, chain, [0]))
    elif len(chain) == ml:
        ms = max(ms, sum(reduce(lambda x, y: x + y, chain, [0])))
    for i, comp in enumerate(unused):
        if not chain:
            if comp[0] == 0:
                ml, ms = search2([comp], unused[:i] + unused[i + 1 :], ml, ms)
            elif comp[1] == 0:
                ml, ms = search2(
                    [[comp[1], comp[0]]], unused[:i] + unused[i + 1 :], ml, ms
                )
        else:
            if comp[0] == chain[-1][1]:
                ml, ms = search2(chain + [comp], unused[:i] + unused[i + 1 :], ml, ms)
            if comp[1] == chain[-1][1]:
                ml, ms = search2(
                    chain + [[comp[1], comp[0]]],
                    unused[:i] + unused[i + 1 :],
                    ml,
                    ms,
                )
    return ml, ms


def part_1(components):
    components = [list(map(int, c.split("/"))) for c in components]
    return search1([], components)


def part_2(components):
    components = [list(map(int, c.split("/"))) for c in components]
    return search2([], components, 0, 0)[1]


if __name__ == "__main__":
    components = load_data(sys.argv[1])
    print(f"Part 1: {part_1(components)}")
    print(f"Part 2: {part_2(components)}")
