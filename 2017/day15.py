def make_gen_a():
    n = 634
    while True:
        n = (n * 16807) % 2147483647
        yield bin(n)[2:].zfill(32)[16:]


def make_gen_b():
    n = 301
    while True:
        n = (n * 48271) % 2147483647
        yield bin(n)[2:].zfill(32)[16:]


if __name__ == "__main__":
    gen_a, gen_b = make_gen_a(), make_gen_b()
    count = 0
    for _ in range(40000000):
        if next(gen_a) == next(gen_b):
            count += 1
    print(count)
