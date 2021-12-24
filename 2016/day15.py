import re
import sys
from functools import reduce

PATTERN = re.compile(r".* (\d+) positions.*position (\d+)\.")


def load_data(path):
    with open(path) as f:
        return [(int(i), int(j)) for i, j in PATTERN.findall(f.read())]


def answer(data):
    # chinese remainder theorem
    # https://brilliant.org/wiki/chinese-remainder-theorem/
    N = reduce(lambda x, y: x * y, [a for a, _ in data])
    solution = sum(
        (-p_i - i) * (y_i := N // n_i) * pow(y_i, -1, n_i)
        for i, (n_i, p_i) in enumerate(data, start=1)
    )
    return solution % N


def part_1(data):
    return answer(data)


def part_2(data):
    return answer(data + [(11, 0)])


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
