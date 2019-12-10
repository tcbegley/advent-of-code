import sys
from collections import Counter
from math import log10


def num_to_digs(n):
    d = int(log10(n)) + 1
    digs = []

    for _ in range(d):
        digs.append(n % 10)
        n //= 10

    digs.reverse()
    return digs


def digs_to_num(n):
    out = 0
    for i in n:
        out *= 10
        out += i
    return out


def validate(digs):
    # digits never decrease
    if not all(i <= j for i, j in zip(digs[:-1], digs[1:])):
        return False
    # two adjacent digits are the same
    if not any(i == j for i, j in zip(digs[:-1], digs[1:])):
        return False

    c = Counter(digs)
    if 2 not in c.values():
        return False

    return True


def answer(path):
    with open(path) as f:
        low, high = map(int, f.read().strip().split("-"))

    valid = set()

    for i in range(low, high + 1):
        digs = num_to_digs(i)
        if validate(digs):
            valid.add(i)

    return len(valid)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
