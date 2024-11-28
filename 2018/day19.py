import math
import sys

# careful analysis of my program reveals that it is counting the sum of factors
# of the value that is in register three the first time the instruction pointer
# has the value 3. there is no guarantee that this will generalise to other
# inputs!


def factorise(n):
    for i in range(1, math.isqrt(n) + 1):
        if n % i == 0:
            yield i
            yield n // i


OPS = {
    "addr": lambda a, b, r: r[a] + r[b],
    "addi": lambda a, b, r: r[a] + b,
    "mulr": lambda a, b, r: r[a] * r[b],
    "muli": lambda a, b, r: r[a] * b,
    "banr": lambda a, b, r: r[a] & r[b],
    "bani": lambda a, b, r: r[a] & b,
    "borr": lambda a, b, r: r[a] | r[b],
    "bori": lambda a, b, r: r[a] | b,
    "setr": lambda a, b, r: r[a],
    "seti": lambda a, b, r: a,
    "gtir": lambda a, b, r: 1 if a > r[b] else 0,
    "gtri": lambda a, b, r: 1 if r[a] > b else 0,
    "gtrr": lambda a, b, r: 1 if r[a] > r[b] else 0,
    "eqir": lambda a, b, r: 1 if a == r[b] else 0,
    "eqri": lambda a, b, r: 1 if r[a] == b else 0,
    "eqrr": lambda a, b, r: 1 if r[a] == r[b] else 0,
}


def load_data(path):
    with open(path) as f:
        instructions = [row.split(" ", 1) for row in f.read().strip().split("\n")]

    instructions = [
        (cmd, tuple(map(int, args.split(" ")))) for cmd, args in instructions
    ]
    instructions[0] = (instructions[0][0], instructions[0][1][0])
    return instructions


def solve(data, part_2=False):
    (cmd, idx), data = data[0], data[1:]
    registers = [0] * 6
    if part_2:
        registers[0] = 1
    ip = registers[idx]

    while ip != 3:
        registers[idx] = ip
        cmd, (a, b, c) = data[ip]
        registers[c] = OPS[cmd](a, b, registers)
        ip = registers[idx]
        ip += 1

    return sum(factorise(registers[3]))


def part_1(data):
    return solve(data)


def part_2(data):
    return solve(data, part_2=True)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
