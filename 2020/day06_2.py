import sys
from functools import reduce
from operator import and_


def answer(path):
    with open(path) as f:
        groups = f.read().strip().split("\n\n")

    return sum(
        len(reduce(and_, [set(a) for a in g.split("\n")])) for g in groups
    )


if __name__ == "__main__":
    print(answer(sys.argv[1]))
