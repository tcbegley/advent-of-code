import re
import sys
from string import ascii_lowercase

LETTERS = "abcdefghjkmnpqrstuvwxyz"
INDEX = {c: i for i, c in enumerate(LETTERS)}
N = len(LETTERS)
TRIPLES = [ascii_lowercase[i : i + 3] for i in range(24)]
PAIR = re.compile(r"([a-z]{1})\1")


def load_data(path):
    with open(path) as f:
        return f.read().strip()


def to_num(s):
    n = 0
    for c in s:
        n = N * n + INDEX[c]
    return n


def to_string(n):
    s = ""
    while n:
        s = LETTERS[n % N] + s
        n //= N
    return "a" * (8 - len(s)) + s


def increment(password):
    return to_string(to_num(password) + 1)


def valid(s):
    return any(trip in s for trip in TRIPLES) and len(PAIR.findall(s)) >= 2


def get_next(password):
    while not valid(password := increment(password)):
        continue

    return password


if __name__ == "__main__":
    password = load_data(sys.argv[1])
    print(f"Part 1: {(password := get_next(password))}")
    print(f"Part 2: {get_next(password)}")
