import re
import sys
from itertools import chain, cycle

ROW_PATTERN = re.compile(r"([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)")


def load_data(path):
    with open(path) as f:
        sequence, rows = f.read().strip().split("\n\n")

    nodes = {}
    for element, left_dest, right_dest in chain(
        *map(ROW_PATTERN.findall, rows.split("\n"))
    ):
        nodes["L", element] = left_dest
        nodes["R", element] = right_dest

    return sequence, nodes


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def lcm(a, b):
    return abs(a * b) // gcd(a, b)


def lcm_multiple(*args):
    result = args[0]
    for arg in args[1:]:
        result = lcm(result, arg)

    return result


def count_steps(sequence, nodes, condition, start="AAA"):
    count = 0
    sequence = cycle(sequence)

    while condition(start):
        start = nodes[next(sequence), start]
        count += 1

    return count


def part_1(sequence, nodes):
    return count_steps(sequence, nodes, condition=lambda el: el != "ZZZ")


def part_2(sequence, nodes):
    starts = set(k for _, k in nodes if k.endswith("A"))
    return lcm_multiple(
        *(
            count_steps(
                sequence,
                nodes,
                condition=lambda el: not el.endswith("Z"),
                start=start,
            )
            for start in starts
        )
    )


if __name__ == "__main__":
    sequence, nodes = load_data(sys.argv[1])
    print(f"Part 1: {part_1(sequence, nodes)}")
    print(f"Part 2: {part_2(sequence, nodes)}")
