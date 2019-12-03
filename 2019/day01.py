import sys


def answer(path):
    with open(path) as f:
        masses = [int(m) // 3 - 2 for m in f.read().strip().split("\n")]
    return sum(masses)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
