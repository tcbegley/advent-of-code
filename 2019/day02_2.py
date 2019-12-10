import sys

from intcode import IntCodeComputer


def answer(path, target=19690720):
    def run_program(noun, verb):
        with open(path) as f:
            program = list(map(int, f.read().strip().split(",")))

        program[1] = noun
        program[2] = verb

        i = IntCodeComputer(program)
        i.compute()

        return i.program[0]

    for i in range(100):
        for j in range(100):
            if run_program(i, j) == target:
                return 100 * i + j


if __name__ == "__main__":
    print(answer(sys.argv[1]))
