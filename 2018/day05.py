import sys
from string import ascii_lowercase, ascii_uppercase

REACT = dict(zip(ascii_uppercase, ascii_lowercase)) | dict(
    zip(ascii_lowercase, ascii_uppercase)
)


def load_data(path):
    with open(path) as f:
        return f.read().strip()


def react(polymer, skip=None):
    stack = []
    for c in polymer:
        if skip is not None and c in skip:
            continue
        elif stack and REACT[c] == stack[-1]:
            stack.pop()
        else:
            stack.append(c)

    return len(stack)


def part_1(polymer):
    return react(polymer)


def part_2(polymer):
    return min(react(polymer, skip) for skip in zip(ascii_uppercase, ascii_lowercase))


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
