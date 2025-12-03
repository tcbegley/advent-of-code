import sys


def load_data(path):
    with open(path) as f:
        return [tuple(int(c) for c in row) for row in f.read().strip().split("\n")]


def get_max_joltage(row, n=2):
    drop = len(row) - n
    stack = []
    for c in row:
        while drop > 0 and stack and stack[-1] < c:
            # if the current number is bigger than one we have in the stack, it will
            # always be beneficial to use that instead as long as you have enough digits
            # remaining (tracked by drop) to fill the stack to the required length
            stack.pop()
            drop -= 1
        stack.append(c)

    return sum(stack[i] * 10 ** (n - 1 - i) for i in range(n))


def part_1(data):
    return sum(get_max_joltage(row) for row in data)


def part_2(data):
    return sum(get_max_joltage(row, n=12) for row in data)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
