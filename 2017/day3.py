import sys
from math import sqrt


def answer(n):
    lookup = [0, 0]
    limit = (int(sqrt(n - 1)) + 1) // 2 + 1
    for i in range(1, limit):
        lookup.extend(
            (list(range(2 * i - 1, i - 1, -1)) + list(range(i + 1, 2 * i + 1)))
            * 4
        )
    return lookup[n]


if __name__ == "__main__":
    print(answer(int(sys.argv[1])))
