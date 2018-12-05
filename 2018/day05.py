import re
import sys
from string import ascii_lowercase, ascii_uppercase


def answer(path):
    with open(path) as f:
        polymer = f.read().strip()
    remove = [f"{a}{b}" for a, b in zip(ascii_lowercase, ascii_uppercase)] + [
        f"{a}{b}" for a, b in zip(ascii_uppercase, ascii_lowercase)
    ]
    pattern = re.compile("|".join(remove))
    while pattern.search(polymer):
        polymer = pattern.sub("", polymer)
    return len(polymer)

if __name__ == "__main__":
    print(answer(sys.argv[1]))
