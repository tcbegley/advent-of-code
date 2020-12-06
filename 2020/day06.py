import sys


def answer(path):
    with open(path) as f:
        groups = f.read().strip().split("\n\n")

    return sum(len(set(g.replace("\n", ""))) for g in groups)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
