import sys


def answer(path):
    with open(path) as f:
        program = list(map(int, f.read().strip().split(",")))

    program[1] = 12
    program[2] = 2

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


if __name__ == "__main__":
    print(answer(sys.argv[1]))
