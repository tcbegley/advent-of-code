import sys
from math import log2


def load_data(path):
    with open(path) as f:
        return int(f.read().strip())


def sieve(target, upper_bound=None, early_stopping=False):
    if upper_bound is None:
        upper_bound = target
    count = [0] * (upper_bound + 1)
    for i in range(1, upper_bound):
        count[i + 1] += i
        if count[i + 1] >= target:
            return i
        for j, k in enumerate(range(2 * i, upper_bound, i)):
            if early_stopping and j >= 50:
                break
            count[k + 1] += i


def part_1(n):
    n //= 10
    # sum of factors of 2^n is 2^(n+1) - 1, so we can get an upper bound
    ub = 2 ** int(log2(n))
    return sieve(n, ub)


def part_2(n):
    n = n // 11 + 1
    return sieve(n, early_stopping=True)


if __name__ == "__main__":
    n = load_data(sys.argv[1])
    print(f"Part 1: {part_1(n)}")
    print(f"Part 2: {part_2(n)}")
