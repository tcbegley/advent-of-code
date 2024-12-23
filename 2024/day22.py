import sys
from collections import Counter


def load_data(path):
    with open(path) as f:
        return [int(n) for n in f.read().strip().split("\n")]


def next_secret(secret):
    secret = (secret << 6 ^ secret) & 16_777_215
    secret = secret >> 5 ^ secret
    return (secret << 11 ^ secret) & 16_777_215


def gen_secret(secret, n_iter=2_000):
    for _ in range(n_iter):
        secret = next_secret(secret)
    return secret


def get_sales(secret, n_iter=2_000) -> Counter:
    sales = Counter()
    diffs = []
    for i in range(n_iter):
        new_secret = next_secret(secret)
        diffs.append(new_secret % 10 - secret % 10)
        secret = new_secret
        if i >= 3 and (k := tuple(diffs[-4:])) not in sales:
            sales[k] += secret % 10

    return sales


def part_1(data):
    return sum(gen_secret(secret) for secret in data)


def part_2(data):
    sales = Counter()
    for secret in data:
        sales += get_sales(secret)

    return sales.most_common(n=1)[0][1]


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
