import sys
from graphlib import TopologicalSorter
from operator import and_, or_, xor

OP_LOOKUP = {"AND": and_, "OR": or_, "XOR": xor}


def load_data(path):
    with open(path) as f:
        values_block, gates_block = f.read().strip().split("\n\n")

    values = {}
    for line in values_block.split("\n"):
        name, value = line.split(": ")
        values[name] = int(value)

    gates = {}
    for line in gates_block.split("\n"):
        left, op, right, _, res = line.split(" ")
        gates[res] = (OP_LOOKUP[op], left, right)

    return values, gates


def part_1(values, gates):
    graph = {}
    for res, (_, left, right) in gates.items():
        graph.setdefault(res, set()).update((left, right))

    for gate in TopologicalSorter(graph).static_order():
        if gate in values:
            continue
        op, left, right = gates[gate]
        values[gate] = op(values[left], values[right])

    return sum(
        values[k] * 2**i
        for i, k in enumerate(sorted(k for k in values if k.startswith("z")))
    )


def find_parent_xor(node, gates):
    for k, (op, left, right) in gates.items():
        if node in (left, right) and op == xor:
            return k


def part_2(values, gates):
    """
    Structure of addition program is as follows

    z00 = x00 ^ y00
    z01 = x01 ^ y01 ^ ((c_out := x00 & y00)
    c_in = c_out
    z02 = x02 ^ y02 ^ ((c_out := (x02 & y02) | ((x01 ^ y01 & c_in)))
    ...
    zAA = xAA ^ yAA ^ ((xAA & yAA) | ((xBB ^ yBB) & c))

    I did this quite manually at first, the below is an attempt to codify and likely
    won't be general...
    """
    assert gates["z00"] in ((xor, "x00", "y00"), (xor, "y00", "x00"))
    # we know that every zAA needs xAA ^ yAA
    xors = {}
    for res, (op, left, right) in gates.items():
        if op == xor:
            left, right = sorted([left, right])
            if left.startswith("x") and right.startswith("y"):
                xors[(left, right)] = res

    swaps = []
    # first op has to be xor, and it's a xor of xor of the inputs + or
    for i in range(1, 45):
        z = f"z{i:02}"
        op, left, right = gates[z]
        key = (f"x{i:02}", f"y{i:02}")
        xor_op = xors[key]
        if op != xor:
            swaps.append(z)
            swaps.append(find_parent_xor(xor_op, gates))
        elif xor_op not in (left, right):
            swaps.append(xor_op)
            for dep in (left, right):
                if gates[dep][0] == and_:
                    swaps.append(dep)

    return ",".join(sorted(swaps))


if __name__ == "__main__":
    values, gates = load_data(sys.argv[1])
    print(f"Part 1: {part_1(values, gates)}")
    print(f"Part 2: {part_2(values, gates)}")
