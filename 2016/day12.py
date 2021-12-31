import sys


class Registers(dict):
    def __missing__(self, key):
        return int(key)


def load_data(path):
    def process_line(line):
        cmd, *args = line.strip().split(" ")
        return cmd, args

    with open(path) as f:
        return [process_line(line) for line in f.readlines()]


def process_instructions(registers, instructions):
    loc = 0
    while loc < len(instructions):
        cmd, args = instructions[loc]
        if cmd == "cpy":
            registers[args[1]] = registers[args[0]]
        elif cmd == "inc":
            registers[args[0]] += 1
        elif cmd == "dec":
            registers[args[0]] -= 1
        elif cmd == "jnz":
            if registers[args[0]] != 0:
                loc += registers[args[1]]
                continue
        loc += 1

    return registers["a"]


def part_1(instructions):
    registers = Registers({"a": 0, "b": 0, "c": 0, "d": 0})
    return process_instructions(registers, instructions)


def part_2(instructions):
    registers = Registers({"a": 0, "b": 0, "c": 1, "d": 0})
    return process_instructions(registers, instructions)


if __name__ == "__main__":
    instructions = load_data(sys.argv[1])
    print(f"Part 1: {part_1(instructions)}")
    print(f"Part 2: {part_2(instructions)}")
