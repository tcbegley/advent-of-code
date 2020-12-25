import sys
from functools import lru_cache
from operator import and_, lshift, or_, rshift


def bit_not(n, numbits=16):
    return (1 << numbits) - 1 - n


OPS = {"AND": and_, "LSHIFT": lshift, "OR": or_, "RSHIFT": rshift}


def load_data(path):
    with open(path) as f:
        return list(map(process_line, f.read().strip().split("\n")))


def maybe_int(s):
    try:
        return int(s)
    except ValueError:
        return s


def process_line(line):
    inputs, output = line.split(" -> ")
    inputs = inputs.split(" ")
    if len(inputs) == 3:
        x, op, y = inputs
        return (OPS[op], [maybe_int(x), maybe_int(y)], output)
    elif len(inputs) == 2:
        return (bit_not, [maybe_int(i) for i in inputs[1:]], output)
    else:
        return (lambda x: x, [maybe_int(i) for i in inputs], output)


def make_resolver(gates):
    @lru_cache
    def resolve(key):
        if isinstance(key, int):
            return key
        op, inputs = gates[key]
        return op(*map(lambda k: resolve(k), inputs))

    return resolve


def part_1(gates):
    gates = {output: (op, inputs) for op, inputs, output in gates}
    resolve = make_resolver(gates)
    return resolve("a")


def part_2(gates, p1):
    gates = {output: (op, inputs) for op, inputs, output in gates}
    gates["b"] = (lambda x: x, [p1])
    resolve = make_resolver(gates)
    return resolve("a")


if __name__ == "__main__":
    gates = load_data(sys.argv[1])
    print(f"Part 1: {(p1 := part_1(gates))}")
    print(f"Part 2: {part_2(gates, p1)}")
