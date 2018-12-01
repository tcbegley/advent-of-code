import sys


def answer(path):
    with open(path) as f:
        steps = [int(i) for i in f.read().strip().split("\n")]
    return sum(steps)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
