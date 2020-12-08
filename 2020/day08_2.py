import sys


def run_program(instructions):
    cursor = 0
    acc = 0
    visited = set()

    while cursor not in visited:
        visited.add(cursor)
        i, v = instructions[cursor]

        if i == "nop":
            cursor += 1
        elif i == "acc":
            acc += v
            cursor += 1
        elif i == "jmp":
            cursor += v

        if cursor == len(instructions):
            # program terminated normally
            return True, acc

    return False, acc


def answer(path):
    with open(path) as f:
        instructions = [
            line.split(" ") for line in f.read().strip().split("\n")
        ]

    instructions = [(x, int(y)) for x, y in instructions]

    for idx, (i, v) in enumerate(instructions):
        if i == "acc":
            continue
        elif i == "nop":
            instructions_copy = instructions[:]
            instructions_copy[idx] = ("jmp", v)
        elif i == "jmp":
            instructions_copy = instructions[:]
            instructions_copy[idx] = ("nop", v)

        terminated, acc = run_program(instructions_copy)

        if terminated:
            return acc


if __name__ == "__main__":
    print(answer(sys.argv[1]))
