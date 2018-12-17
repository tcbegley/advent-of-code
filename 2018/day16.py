import re
import sys

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
    count = 0

    for s in samples:
        n = 0
        b, i, a = s
        for op in ops.values():
            if apply(i[1], i[2], i[3], b[:], op) == a:
                n += 1
            if n >= 3:
                count += 1
                break
    return count


if __name__ == "__main__":
    print(answer(sys.argv[1]))
