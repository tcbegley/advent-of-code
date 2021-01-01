import re
import sys

NUMBERS = re.compile(r"\d+")


def load_data(path):
    with open(path) as f:
        return map(int, NUMBERS.findall(f.read()))


def make_gen_a(start, multiples_only=False):
    n = start
    while True:
        n = (n * 16807) % 2147483647
        if not multiples_only or n % 4 == 0:
            yield bin(n)[2:].zfill(32)[16:]


def make_gen_b(start, multiples_only=False):
    n = start
    while True:
        n = (n * 48271) % 2147483647
        if not multiples_only or n % 8 == 0:
            yield bin(n)[2:].zfill(32)[16:]


def part_1(a, b):
    gen_a, gen_b = make_gen_a(a), make_gen_b(b)
    count = 0
    for _ in range(40_000_000):
        if next(gen_a) == next(gen_b):
            count += 1
    return count


def part_2(a, b):
    gen_a, gen_b = make_gen_a(a, True), make_gen_b(b, True)
    count = 0
    for _ in range(5_000_000):
        if next(gen_a) == next(gen_b):
            count += 1
    return count


if __name__ == "__main__":
    a, b = load_data(sys.argv[1])
    print(f"Part 1: {part_1(a, b)}")
    print(f"Part 2: {part_2(a, b)}")
