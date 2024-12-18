import re
import sys

NUMBER_PATTERN = re.compile(r"\d+")


class Computer:
    def __init__(self, registers):
        self.r = [*registers]
        self.ip = 0
        self.output = []

    def combo(self, op):
        if 0 <= op <= 3:
            return op
        elif 4 <= op <= 6:
            return self.r[op - 4]
        raise ValueError("Invalid combo op")

    def instruction(self, ins, op):
        match ins:
            case 0:
                self.r[0] //= 2 ** self.combo(op)
            case 1:
                self.r[1] ^= op
            case 2:
                self.r[1] = self.combo(op) & 7
            case 3:
                if self.r[0] != 0:
                    self.ip = op
                    return
            case 4:
                self.r[1] ^= self.r[2]
            case 5:
                self.output.append(self.combo(op) & 7)
            case 6:
                self.r[1] = self.r[0] // 2 ** self.combo(op)
            case 7:
                self.r[2] = self.r[0] // 2 ** self.combo(op)

        self.ip += 2

    def process(self, program):
        self.output = []
        self.ip = 0

        while 0 <= self.ip < len(program):
            # print(f"{self.ip=}, {self.r=}, {self.output}")
            self.instruction(*program[self.ip : self.ip + 2])

        return ",".join(map(str, self.output))


def get_ints(s):
    return [int(n) for n in NUMBER_PATTERN.findall(s)]


def load_data(path):
    with open(path) as f:
        registers, program = f.read().strip().split("\n\n")

    return get_ints(registers), get_ints(program)


def compute(r0):
    # this function is equivalent to my program, it is not general
    while r0 != 0:
        r1 = (r0 & 7) ^ 2
        yield ((r1 ^ (r0 // 2**r1)) ^ 7) % 8
        r0 //= 8


def invert(target, a):
    # this function inverts my program, i got stuck for a while because it turns out
    # you need to allow for backtracking, i.e. there is more than one choice you can
    # make to generate each digit, and some choices make the remaining digits impossible
    if len(target) == 0:
        return a
    for i in range(8):
        r1 = i ^ 2
        if ((r1 ^ ((8 * a + i) // 2**r1)) ^ 7) & 7 == target[-1]:
            if (res := invert(target[:-1], 8 * a + i)) is not None:
                return res


def part_1(registers, program):
    computer = Computer(registers)
    answer = computer.process(program)
    assert ",".join(map(str, compute(registers[0]))) == answer
    return answer


def part_2(_, program):
    r0 = invert(program, 0)
    assert list(compute(r0)) == program
    return r0


if __name__ == "__main__":
    registers, program = load_data(sys.argv[1])
    print(f"Part 1: {part_1(registers[:], program)}")
    print(f"Part 2: {part_2(registers, program)}")
