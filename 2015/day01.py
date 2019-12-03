import sys


def answer(path):
    with open(path) as f:
        instructions = f.read()
    return instructions.count("(") - instructions.count(")")


if __name__ == "__main__":
    print(answer(sys.argv[1]))
