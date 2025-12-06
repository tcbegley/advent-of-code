import sys
from functools import reduce
from operator import add, mul

OP_LOOKUP = {"+": add, "*": mul}


def pad_rows(rows):
    row_length = max(len(row) for row in rows)
    return [row + " " * (row_length - len(row)) for row in rows]


def parse_numbers(rows, prev_idx, idx, col_oriented):
    if col_oriented:
        return tuple(
            int("".join(row[i] for row in rows[:-1])) for i in range(prev_idx + 1, idx)
        )
    return tuple(int(row[prev_idx + 1 : idx]) for row in rows[:-1])


def load_data(path, col_oriented=False):
    with open(path) as f:
        rows = pad_rows(f.read().strip().split("\n"))

    numbers = []
    ops = []
    idx = 0
    prev_idx = -1
    while idx < len(rows[0]):
        if all(row[idx] == " " for row in rows):
            numbers.append(parse_numbers(rows, prev_idx, idx, col_oriented))
            ops.append(rows[-1][prev_idx + 1 : idx].strip())
            prev_idx = idx
        idx += 1

    numbers.append(parse_numbers(rows, prev_idx, idx, col_oriented))
    ops.append(rows[-1][prev_idx:idx].strip())

    return numbers, ops


def compute(numbers, ops):
    return sum(
        reduce(OP_LOOKUP[op], nums) for nums, op in zip(numbers, ops, strict=True)
    )


if __name__ == "__main__":
    numbers, ops = load_data(sys.argv[1])
    print(f"Part 1: {compute(numbers, ops)}")
    numbers, ops = load_data(sys.argv[1], col_oriented=True)
    print(f"Part 2: {compute(numbers, ops)}")
