import re
import sys
from functools import reduce

ops = {
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


def parse_sample(s):
    s = s.split("\n")
    b = [int(i) for i in re.search(r"\[([\d, ]+)\]", s[0]).group(1).split(",")]
    i = [int(i) for i in s[1].split(" ")]
    a = [int(i) for i in re.search(r"\[([\d, ]+)\]", s[2]).group(1).split(",")]
    return (b, i, a)


def apply(a, b, c, r, op):
    r[c] = op(a, b, r)
    return r


def answer(path):
    with open(path) as f:
        samples, test = f.read().strip().split("\n\n\n")

    samples = samples.split("\n\n")
    test = [
        [int(i) for i in line.split(" ")] for line in test.strip().split("\n")
    ]

    samples = [parse_sample(s) for s in samples]
    constraints = {i: [] for i in range(16)}

    for s in samples:
        b, i, a = s
        constraint = set()
        for op_name, op in ops.items():
            if apply(i[1], i[2], i[3], b[:], op) == a:
                constraint.add(op_name)
        constraints[i[0]].append(constraint)

    for opcode in constraints.keys():
        constraints[opcode] = reduce(lambda x, y: x & y, constraints[opcode])

    opcodes = {}

    while len(opcodes) < 16:
        unique = {k: v.pop() for k, v in constraints.items() if len(v) == 1}
        opcodes.update(unique)
        for allowed in constraints.values():
            for v in unique.values():
                if v in allowed:
                    allowed.remove(v)

    r = [0] * 4
    for t in test:
        op, a, b, c = t
        r = apply(a, b, c, r, ops[opcodes[op]])

    return r


if __name__ == "__main__":
    print(answer(sys.argv[1]))
