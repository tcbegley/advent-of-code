import re
import sys
from functools import lru_cache


def score(state, left):
    total = 0
    for i, p in enumerate(state):
        if p == "#":
            total += i + left
    return total


def build_evolver(rules):
    TRIM = re.compile(r"#[.#]*#")

    @lru_cache(None)
    def evolve(s):
        left = 0

        left += s.index("#")
        s = TRIM.search(s).group(0)

        leftmost = [rules["." * (5 - i) + s[:i]] for i in range(1, 5)]
        if "#" in leftmost:
            lindex = leftmost.index("#")
        else:
            lindex = 5

        left += lindex - 2

        inner = [rules[s[i - 2 : i + 3]] for i in range(2, len(s) - 2)]

        rightmost = [rules[s[-i:] + "." * (5 - i)] for i in range(4, 0, -1)]
        if "#" in rightmost:
            rindex = 3 - list(reversed(rightmost)).index("#")
        else:
            rindex = -1
        return (
            "".join(leftmost[lindex:] + inner + rightmost[: rindex + 1]),
            left,
        )

    return evolve


def answer(path):
    with open(path) as f:
        lines = f.read().strip().split("\n")

    init_state = re.search(r"[.#]+", lines[0]).group(0)

    state = init_state
    left = 0

    rules = {}
    for line in lines[2:]:
        k, v = line.split(" => ")
        rules[k] = v

    evolve = build_evolver(rules)

    prev = 0
    diff = 0

    # evolve until we've seen something twice
    for gen in range(200):
        state, l_shift = evolve(state)
        left += l_shift
        s = score(state, left)
        diff = s - prev
        prev = s

    return score(state, left) + diff * (50000000000 - 200)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
