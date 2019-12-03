import sys


def answer(path):
    with open(path) as f:
        instructions = f.read()
    floor = 0
    for i, instruction in enumerate(instructions):
        if instruction == "(":
            floor += 1
        else:
            floor -= 1
        if floor < 0:
            return i + 1
    return None


if __name__ == "__main__":
    print(answer(sys.argv[1]))
