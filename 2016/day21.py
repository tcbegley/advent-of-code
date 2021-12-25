import sys
from collections import deque


def load_data(path):
    def process_line(line):
        words = line.strip().split(" ")
        if line.startswith("swap position"):
            return "sp", (int(words[2]), int(words[5]))
        elif line.startswith("swap letter"):
            return "sl", (words[2], words[5])
        elif line.startswith("rotate"):
            if words[1] == "right":
                return "rot", (int(words[2]),)
            elif words[1] == "left":
                return "rot", (-int(words[2]),)
            return "rot", (words[6],)
        elif line.startswith("reverse"):
            return "rev", (int(words[2]), int(words[4]))
        return "mov", (int(words[2]), int(words[5]))

    with open(path) as f:
        return [process_line(line) for line in f.readlines()]


def apply(cmd, args, passcode):
    if cmd == "sp":
        passcode[args[0]], passcode[args[1]] = (
            passcode[args[1]],
            passcode[args[0]],
        )
    elif cmd == "sl":
        i1 = passcode.index(args[0])
        i2 = passcode.index(args[1])
        passcode[i1], passcode[i2] = passcode[i2], passcode[i1]
    elif cmd == "rot":
        n = args[0]
        if not isinstance(n, int):
            n = passcode.index(n)
            if n >= 4:
                n += 2
            else:
                n += 1
        passcode.rotate(n)
    elif cmd == "rev":
        stack = []
        passcode.rotate(-args[0])
        for _ in range(1 + args[1] - args[0]):
            stack.append(passcode.popleft())

        while stack:
            passcode.append(stack.pop())

        passcode.rotate(1 + args[1])
    elif cmd == "mov":
        passcode.rotate(-args[0])
        tmp = passcode.popleft()
        passcode.rotate(args[0] - args[1])
        passcode.appendleft(tmp)
        passcode.rotate(args[1])


def invert(cmd, args, passcode):
    if cmd == "rot":
        inv = [-1, -1, 2, -2, 1, -3, 0, -4]
        if not isinstance(args[0], int):
            n = passcode.index(args[0])
            return "rot", (inv[n],)
        return "rot", (-args[0],)
    elif cmd == "mov":
        return "mov", (args[1], args[0])

    return cmd, args


def part_1(instructions):
    passcode = deque("abcdefgh")
    steps = []
    steps.append("".join(passcode))

    for cmd, args in instructions:
        apply(cmd, args, passcode)
        steps.append("".join(passcode))

    return "".join(passcode)


def part_2(instructions):
    passcode = deque("fbgdceah")
    steps = []
    steps.append("".join(passcode))

    for cmd, args in reversed(instructions):
        cmd, args = invert(cmd, args, passcode)
        apply(cmd, args, passcode)
        steps.append("".join(passcode))

    return "".join(passcode)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
