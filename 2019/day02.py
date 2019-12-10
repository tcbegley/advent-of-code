import sys

from intcode import IntCodeComputer


def answer(path):
    with open(path) as f:
        program = list(map(int, f.read().strip().split(",")))

    program[1] = 12
    program[2] = 2

    i = IntCodeComputer(program)
    i.compute()

    return i.program[0]


if __name__ == "__main__":
    print(answer(sys.argv[1]))
