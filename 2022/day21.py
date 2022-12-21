import sys
from graphlib import TopologicalSorter
from operator import add, floordiv, mul, sub

OPS = {"+": add, "-": sub, "*": mul, "/": floordiv}
INVERSE_OPS = {"-": add, "+": sub, "/": mul, "*": floordiv}


def load_data(path):
    with open(path) as f:
        data = [row.split(": ") for row in f.read().strip().split("\n")]
    return dict((monkey, command.split(" ")) for monkey, command in data)


def parse_dependencies(data):
    values = {}
    dependencies = {}
    for monkey, command in data.items():
        match command:
            case [val]:
                values[monkey] = int(val)
            case [a, _, b]:
                dependencies.setdefault(monkey, set()).update((a, b))
    return values, dependencies


def process(values, dependencies, hook):
    # evalute each monkey's value using topological order
    # in part 2 when we have a placeholder value humn, we keep track of the
    # operations being performed and will later invert
    for monkey in TopologicalSorter(dependencies).static_order():
        if monkey in values:
            continue
        a, op, b = data[monkey]
        if monkey == "root":
            return hook(op, values[a], values[b])
        else:
            try:
                values[monkey] = OPS[op](int(values[a]), int(values[b]))
            except (ValueError, TypeError):
                values[monkey] = [values[a], op, values[b]]


def invert(a, b):
    if isinstance(a, int):
        a, b = b, a
    if a == "humn" and isinstance(b, int):
        return b
    a1, op, a2 = a
    if isinstance(a1, int):
        # inverting division and subtraction keeping right operand is delicate
        # a - b = c  ->  b = a - c
        # a / b = c  ->  b = a / c
        if op == "/":
            return invert(a2, floordiv(a1, b))
        elif op == "-":
            return invert(a2, sub(a1, b))
        return invert(a2, INVERSE_OPS[op](b, a1))
    elif isinstance(a2, int):
        return invert(a1, INVERSE_OPS[op](b, a2))


def part_1(data):
    def hook(op, a, b):
        return OPS[op](a, b)

    values, dependencies = parse_dependencies(data)
    return process(values, dependencies, hook)


def part_2(data):
    def hook(_, a, b):
        return invert(a, b)

    values, dependencies = parse_dependencies(data)
    values["humn"] = "humn"
    return process(values, dependencies, hook)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
