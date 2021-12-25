import sys


def load_data(path):
    with open(path) as f:
        return f.read().strip()


def to_int(data):
    return int("".join("1" if c == "^" else "0" for c in data), 2)


def next_row(row, n_digits):
    return ((row << 1) ^ (row >> 1)) & ((1 << n_digits) - 1)


def count_zeros(row, n_digits):
    return n_digits - row.bit_count()


def answer(data, n=40):
    n_digits = len(data)
    data = to_int(data)

    count = count_zeros(data, n_digits)
    for _ in range(n - 1):
        data = next_row(data, n_digits)
        count += count_zeros(data, n_digits)

    return count


def part_1(data):
    return answer(data, n=40)


def part_2(data):
    return answer(data, n=400_000)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
