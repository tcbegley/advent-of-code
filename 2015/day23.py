import sys


def load_data(path):
    with open(path) as f:
        instructions = [
            line.split(" ", 1) for line in f.read().strip().split("\n")
        ]

    for i in range(len(instructions)):
        op, args = instructions[i]
        if "," in args:
            reg, jmp = args.split(", ")
            instructions[i] = [op, [reg, int(jmp)]]
        elif op == "jmp":
            instructions[i] = [op, int(args)]

    return instructions


def compute(instructions, a=0):
    ops = {
        "hlf": lambda x: x // 2,
        "tpl": lambda x: 3 * x,
        "inc": lambda x: x + 1,
    }
    registers = {"a": a, "b": 0}

    cursor = 0

    while cursor < len(instructions):
        op, args = instructions[cursor]
        if op == "jmp":
            cursor += args
        elif op == "jio":
            if registers[args[0]] == 1:
                cursor += args[1]
            else:
                cursor += 1
        elif op == "jie":
            if registers[args[0]] % 2 == 0:
                cursor += args[1]
            else:
                cursor += 1
        else:
            registers[args] = ops[op](registers[args])
            cursor += 1

    return registers["b"]


def part_1(instructions):
    return compute(instructions)


def part_2(instructions):
    return compute(instructions, 1)


if __name__ == "__main__":
    instructions = load_data(sys.argv[1])
    print(f"Part 1: {part_1(instructions)}")
    print(f"Part 2: {part_2(instructions)}")
