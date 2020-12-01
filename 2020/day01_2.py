import sys


def answer(path):
    with open(path) as f:
        numbers = set(int(n) for n in f.read().strip().split("\n"))

    for i in numbers:
        for j in numbers:
            if (k := 2020 - i - j) in numbers:
                return i * j * k


if __name__ == "__main__":
    print(answer(sys.argv[1]))
