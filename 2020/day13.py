import sys
from functools import reduce


def load_data(path):
    with open(path) as f:
        ts, buses = f.read().strip().split("\n")

    ts = int(ts)
    buses = [(i, int(b)) for i, b in enumerate(buses.split(",")) if b != "x"]

    return ts, buses


def part_1(ts, buses):
    min_b, min_ts = min([(b, (ts // b + 1) * b) for _, b in buses], key=lambda x: x[1])
    return min_b * (min_ts - ts)


def part_2(buses):
    # application of chinese remainder theorem
    N = reduce(lambda a, b: a * b, [b[1] for b in buses])
    return sum(-o * (n_i := N // p) * pow(n_i, -1, p) for o, p in buses) % N


if __name__ == "__main__":
    ts, buses = load_data(sys.argv[1])
    print(f"Part 1: {part_1(ts, buses)}")
    print(f"Part 2: {part_2(buses)}")
