import sys

import numpy as np


def answer(path):
    with open(path) as f:
        codes = [np.array(list(c)) for c in f.read().strip().split("\n")]

    n = len(codes[0])

    for i in range(len(codes)):
        for j in range(i + 1, len(codes)):
            if sum(codes[i] == codes[j]) == n - 1:
                return "".join(codes[i][codes[i] == codes[j]])


if __name__ == "__main__":
    print(answer(sys.argv[1]))
