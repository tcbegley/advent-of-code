import sys


def answer(path):
    with open(path) as f:
        instructions = [
            line.split(" ") for line in f.read().strip().split("\n")
        ]

    instructions = [(x, int(y)) for x, y in instructions]

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

    return acc


if __name__ == "__main__":
    print(answer(sys.argv[1]))
