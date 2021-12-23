import hashlib
import sys
from collections import defaultdict
from functools import cache


def load_data(path):
    with open(path) as f:
        return f.read().strip()


@cache
def get_hash(data, n):
    return hashlib.md5(f"{data}{n}".encode()).hexdigest()


@cache
def get_stretched_hash(data, n):
    data = f"{data}{n}"
    for _ in range(2017):
        data = hashlib.md5(data.encode()).hexdigest()
    return data


def get_triple(h):
    current, run = h[0], 1
    for c in h[1:]:
        if c == current:
            run += 1
        else:
            if run >= 3:
                return current
            current, run = c, 1

    if run >= 3:
        return current

    return None


def get_quintuples(h):
    current, run = h[0], 1
    quintuples = []
    for c in h[1:]:
        if c == current:
            run += 1
        else:
            if run >= 5:
                quintuples.append(current)
            current, run = c, 1

    if run >= 5:
        quintuples.append(current)

    return quintuples


def answer(data, get_hash):
    fives = defaultdict(list)

    for i in range(1, 1001):
        for c in get_quintuples(get_hash(data, i)):
            fives[c].append(i)

    n = 0
    keys = []
    while len(keys) < 64:
        if (c := get_triple(get_hash(data, n))) is not None:
            for i in fives[c]:
                if n < i <= n + 1000:
                    keys.append(n)
                    break
                elif i > n + 1000:
                    break

        n += 1
        for c in get_quintuples(get_hash(data, n + 1000)):
            fives[c].append(n + 1000)

    return keys[-1]


def part_1(data):
    return answer(data, get_hash)


def part_2(data):
    return answer(data, get_stretched_hash)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
