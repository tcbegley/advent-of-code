import sys

from intcode import IntCodeComputer


def answer(path):
    with open(path) as f:
        program = list(map(int, f.read().strip().split(",")))

    i = IntCodeComputer(program)
    i.compute()


if __name__ == "__main__":
    answer(sys.argv[1])
