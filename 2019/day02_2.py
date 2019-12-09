import sys


def answer(path, target=19690720):
    def run_program(noun, verb):
        with open(path) as f:
            program = list(map(int, f.read().strip().split(",")))

        program[1] = noun
        program[2] = verb

        def op1(in1, in2, in3):
            program[in3] = program[in1] + program[in2]

        def op2(in1, in2, in3):
            program[in3] = program[in1] * program[in2]

        i = 0

        while program[i] != 99:
            if program[i] == 1:
                op1(*program[i + 1 : i + 4])
            elif program[i] == 2:
                op2(*program[i + 1 : i + 4])

            i += 4

        return program[0]

    for i in range(100):
        for j in range(100):
            if run_program(i, j) == target:
                return 100 * i + j


if __name__ == "__main__":
    print(answer(sys.argv[1]))
