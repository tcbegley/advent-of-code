import re
import sys


def answer(path):
    with open(path) as f:
        passes = re.sub(r"F|L", "0", f.read().strip())
        passes = re.sub(r"B|R", "1", passes)
        passes = passes.split("\n")

    passes = [int(p, 2) for p in passes]

    return next(iter(set(range(min(passes), max(passes) + 1)) - set(passes)))


if __name__ == "__main__":
    print(answer(sys.argv[1]))
