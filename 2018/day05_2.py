import re
import sys
from string import ascii_lowercase, ascii_uppercase


def answer(path):
    with open(path) as f:
        polymer = f.read().strip()
    remove = [f"{a}{b}" for a, b in zip(ascii_lowercase, ascii_uppercase)] + [
        f"{a}{b}" for a, b in zip(ascii_uppercase, ascii_lowercase)
    ]
    types = [f"{a}|{b}" for a,b in zip(ascii_lowercase, ascii_uppercase)]

    min_length = float("inf")

    pattern = re.compile("|".join(remove))

    for t in types:
        p = re.sub(t, "", polymer)
        while pattern.search(p):
            p = pattern.sub("", p)
        l = len(p)
        if l < min_length:
            min_length = l
    return min_length

if __name__ == "__main__":
    print(answer(sys.argv[1]))
