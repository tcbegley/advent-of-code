import sys

# r0 = r1 = r2 = r3 = r4 = r5 = 0

# while True:
#     r5 = r2 | 2 ** 16
#     r2 = 4_843_319 + (r5 & 255)
#     r2 &= 16_777_215  # = 2^24 - 1
#     r2 *= 65_899
#     r2 &= 16_777_215  # = 2^24 - 1

#     if r5 < 256:
#         if r0 == r2:
#             print("success!")
#             break
#         else:
#             continue
#     else:
#         r4 = 0
#         while True:
#             r3 = 256 * (r4 + 1)
#             if 256 * (r4 + 1) > r5:
#                 r5 = r4


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
            print(steps)
            return registers[2]
        registers[c] = OPS[cmd](a, b, registers)
        ip = registers[idx]
        ip += 1
        steps += 1


def part_2(data):
    (cmd, idx), *data = data
    registers = [0] * 6

    steps = 0
    ip = registers[idx]

    last_value = None
    seen = set()

    while steps < 1_000_000_000:
        registers[idx] = ip
        cmd, (a, b, c) = data[ip]
        if cmd == "eqrr":
            print("Hit eqrr")
            val = registers[2]
            if val in seen:
                return last_value
            seen.add(val)
            last_value = val
        registers[c] = OPS[cmd](a, b, registers)
        ip = registers[idx]
        ip += 1
        steps += 1

    print(len(seen))


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    data = load_data(sys.argv[1])
    print(f"Part 2: {part_2(data)}")
