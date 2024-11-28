import re
import sys

NUMBER = re.compile(r"-?\d+")
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
        samples, tests = f.read().strip().split("\n\n\n\n")

    samples = [
        tuple(
            list(x)
            for x in zip(*([iter([int(i) for i in NUMBER.findall(sample)])] * 4))
        )
        for sample in samples.split("\n\n")
    ]
    tests = [[int(i) for i in NUMBER.findall(test)] for test in tests.split("\n")]
    return samples, tests


def apply_op(op, a, b, c, r):
    r[c] = op(a, b, r)
    return r


def part_1(samples):
    return sum(
        sum(apply_op(op, *instructions[1:], before[:]) == after for op in OPS.values())
        >= 3
        for before, instructions, after in samples
    )


def part_2(samples, tests):
    possible = {i: set(OPS) for i in range(16)}
    for before, instructions, after in samples:
        for op_name, op in OPS.items():
            if (
                op_name in possible[instructions[0]]
                and apply_op(op, *instructions[1:], before[:]) != after
            ):
                possible[instructions[0]].remove(op_name)

    opcodes = {}
    while len(opcodes) < 16:
        for i, candidates in tuple(possible.items()):
            if len(candidates) == 1:
                opcode = candidates.pop()
                for j, v in possible.items():
                    if j != i and opcode in v:
                        v.remove(opcode)
                opcodes[i] = opcode
                del possible[i]
                continue

    registers = [0] * 4
    for op, a, b, c in tests:
        registers = apply_op(OPS[opcodes[op]], a, b, c, registers)

    return registers[0]


if __name__ == "__main__":
    samples, tests = load_data(sys.argv[1])
    print(f"Part 1: {part_1(samples)}")
    print(f"Part 2: {part_2(samples, tests)}")
