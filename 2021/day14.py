import sys
from collections import Counter
from functools import cache, reduce


def load_data(path):
    with open(path) as f:
        polymer, rules = f.read().strip().split("\n\n")

    rules = dict(rule.strip().split(" -> ") for rule in rules.split("\n"))
    return polymer, rules


def add_dicts(*args):
    def add_two(d1, d2):
        keys = set(d1.keys()) | set(d2.keys())
        return {k: d1.get(k, 0) + d2.get(k, 0) for k in keys}

    return reduce(add_two, args)


def answer(polymer, rules, iterations):
    @cache
    def counts(pair, iterations):
        # count characters that will be inserted between `pair` in the given
        # number of iterations
        if iterations == 0:
            return {}
        c = rules[pair]
        return add_dicts(
            {c: 1},
            counts(pair[0] + c, iterations - 1),
            counts(c + pair[1], iterations - 1),
        )

    counts = sorted(
        add_dicts(
            Counter(polymer),  # counts only counts inserted chars
            *[counts(x + y, iterations) for x, y in zip(polymer, polymer[1:])],
        ).values()
    )
    return counts[-1] - counts[0]


def part_1(polymer, rules):
    return answer(polymer, rules, iterations=10)


def part_2(polymer, rules):
    return answer(polymer, rules, iterations=40)


if __name__ == "__main__":
    polymer, rules = load_data(sys.argv[1])
    print(f"Part 1: {part_1(polymer, rules)}")
    print(f"Part 2: {part_2(polymer, rules)}")
