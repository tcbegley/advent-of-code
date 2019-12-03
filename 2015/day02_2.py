import sys


def required(dim):
    a, b, c = sorted(dim)
    return 2 * (a + b) + a * b * c


def answer(path):
    with open(path) as f:
        dims = [
            [int(i) for i in line.split("x")]
            for line in f.read().strip().split("\n")
        ]

    return sum(required(dim) for dim in dims)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
