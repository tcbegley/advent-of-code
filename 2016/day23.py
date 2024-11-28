import sys
from copy import deepcopy

TOGGLE_MAP = {
    "inc": "dec",
    "dec": "inc",
    "tgl": "inc",
    "jnz": "cpy",
    "cpy": "jnz",
}


class Registers(dict):
    def __missing__(self, key):
        # if key isn't in dictionary, return integer value of key instead
        return key


def load_data(path):
    def maybe_int(x):
        try:
            return int(x)
        except ValueError:
            return x

    def process_line(line):
        cmd, *args = line.strip().split(" ")
        return [cmd, [maybe_int(x) for x in args]]

    with open(path) as f:
        return [process_line(line) for line in f.readlines()]


def optimise(instructions):
    # https://en.wikipedia.org/wiki/Peephole_optimization
    # if we have a block like this

    # cpy b c
    # inc a
    # dec c
    # jnz c -2
    # dec d
    # jnz d -5

    # result of this is
    # a += b * d
    # b = b
    # c = 0
    # d = 0

    for loc in range(len(instructions) - 6):
        block = instructions[loc : loc + 6]

        if (
            [cmd for cmd, _ in block] == ["cpy", "inc", "dec", "jnz", "dec", "jnz"]
            and block[3][1][1] == -2
            and block[5][1][1] == -5
        ):
            new_block = [
                [
                    "mul",
                    [block[0][1][0], block[4][1][0], block[1][1][0]],
                ],
                ["cpy", [0, block[2][1][0]]],
                ["cpy", [0, block[4][1][0]]],
            ] + [["jnz", [0, 0]] for _ in range(3)]  # keep block size the same
            instructions[loc : loc + 6] = new_block
    return instructions


def process_instructions(registers, instructions):
    instructions = optimise(instructions)
    loc = 0
    while loc < len(instructions):
        cmd, args = instructions[loc]
        if cmd == "cpy":
            if args[1] in registers:
                registers[args[1]] = registers[args[0]]
        elif cmd == "inc":
            registers[args[0]] += 1
        elif cmd == "dec":
            registers[args[0]] -= 1
        elif cmd == "jnz":
            if registers[args[0]] != 0:
                loc += registers[args[1]]
                continue
        elif cmd == "tgl":
            target_loc = loc + registers[args[0]]

            if 0 <= target_loc < len(instructions):
                instructions[target_loc][0] = TOGGLE_MAP[instructions[target_loc][0]]
                instructions = optimise(instructions)
        elif cmd == "mul":
            registers[args[2]] += registers[args[0]] * registers[args[1]]

        loc += 1

    return registers["a"]


def part_1(instructions):
    registers = Registers({"a": 7, "b": 0, "c": 0, "d": 0})
    return process_instructions(registers, instructions)


def part_2(instructions):
    registers = Registers({"a": 12, "b": 0, "c": 0, "d": 0})
    return process_instructions(registers, instructions)


if __name__ == "__main__":
    instructions = load_data(sys.argv[1])
    print(f"Part 1: {part_1(deepcopy(instructions))}")
    print(f"Part 2: {part_2(instructions)}")
