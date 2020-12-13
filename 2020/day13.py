import sys
from functools import reduce


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def lcm(a, b):
    return a * b // gcd(a, b)


def extended_gcd(a, b):
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_s, old_t


def load_data(path):
    with open(path) as f:
        ts, buses = f.read().strip().split("\n")

    ts = int(ts)
    buses = [(i, int(b)) for i, b in enumerate(buses.split(",")) if b != "x"]

    return ts, buses


def part_1(ts, buses):
    min_b, min_ts = min(
        [(b, (ts // b + 1) * b) for _, b in buses], key=lambda x: x[1]
    )
    return min_b * (min_ts - ts)


def part_2(buses):
    def compare_2(bus1, bus2):
        offset1, id1 = bus1
        offset2, id2 = bus2

        a, b = extended_gcd(id1, id2)
        lcm_ = lcm(id1, id2)

        t = (offset2 - offset1) * a * id1 + offset1

        bus3 = (t % lcm_, lcm_)
        return bus3

    offset, period = reduce(compare_2, buses)
    return period - offset


if __name__ == "__main__":
    ts, buses = load_data(sys.argv[1])
    print(f"Part 1: {part_1(ts, buses)}")
    print(f"Part 2: {part_2(buses)}")
