import sys


def answer(path):
    with open(path) as f:
        numbers = set(int(n) for n in f.read().strip().split("\n"))

    for i in numbers:
        if (j := 2020 - i) in numbers:
            return i * j


if __name__ == "__main__":
    print(answer(sys.argv[1]))
