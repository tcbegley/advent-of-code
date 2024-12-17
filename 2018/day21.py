"""
This file contains a general solution, but it will take some time to run (recommend
using PyPy if you try it). It also contains an optimised solution where I manually
converted my input into actual Python code, and simplified some of the loops into single
division operations etc. These return almost instantly.
"""

import sys

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


def part_1(data):
    (cmd, idx), *data = data
    registers = [0] * 6

    steps = 0
    ip = registers[idx]

    while steps < 10_000_000:
        registers[idx] = ip
        cmd, (a, b, c) = data[ip]
        if cmd == "eqrr":
            return registers[2]
        registers[c] = OPS[cmd](a, b, registers)
        ip = registers[idx]
        ip += 1
        steps += 1


def part_2(data):
    (cmd, idx), *data = data
    registers = [0] * 6

    ip = registers[idx]

    last_value = None
    seen = set()

    while True:
        registers[idx] = ip
        cmd, (a, b, c) = data[ip]
        if cmd == "eqrr":
            val = registers[2]
            if val in seen:
                return last_value
            seen.add(val)
            last_value = val
        registers[c] = OPS[cmd](a, b, registers)
        ip = registers[idx]
        ip += 1


def part_1_opt():
    r2 = 0
    while True:
        r5 = r2 | 65_536
        r2 = 4_843_319
        while True:
            r2 = ((r2 + (r5 & 255)) * 65_899) & 0xFFFFFF
            if r5 < 256:
                return r2
            r5 //= 256


def part_2_opt():
    seen = set()
    last = None
    r2 = 0
    while True:
        r5 = r2 | 65_536
        r2 = 4_843_319
        while True:
            r2 = ((r2 + (r5 & 255)) * 65_899) & 0xFFFFFF
            if r5 < 256:
                if r2 in seen:
                    return last
                last = r2
                seen.add(r2)
                break
            r5 //= 256


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    # print(f"Part 1: {part_1(data)}")
    print(f"Part 1: {part_1_opt()}")
    data = load_data(sys.argv[1])
    # print(f"Part 2: {part_2(data)}")
    print(f"Part 2: {part_2_opt()}")
