import re
import sys


def answer(path):
    with open(path) as f:
        lines = f.read().strip().split("\n")

    state = f"{'.'*20}{re.search(r'[.#]+', lines[0]).group(0)}{'.'*20}"

    n = len(state)

    rules = {}
    for line in lines[2:]:
        k, v = line.split(" => ")
        rules[k] = v

    for gen in range(20):
        print(state)
        new_state = ".."
        for i in range(2, n - 2):
            new_state += rules[state[i - 2 : i + 3]]
        state = new_state + ".."

    total = 0
    for i, p in enumerate(state):
        if p == "#":
            total += i - 20

    return total


if __name__ == "__main__":
    print(answer(sys.argv[1]))
