import re
import sys
from functools import lru_cache

COLOUR_PATTERN = re.compile(r"^(\d+) (.*) bags?$")


def extract_colours(s):
    s = s.rstrip(".")
    if s == "no other bags":
        return []

    s = s.split(", ")
    s = [COLOUR_PATTERN.match(x) for x in s]
    return [(int(m.group(1)), m.group(2)) for m in s if m]


def make_bag_counter(rules):
    @lru_cache
    def count_bags(colour):
        if len(rules[colour]) == 0:
            # only this bag counts
            return 1
        return sum(cnt * count_bags(clr) for cnt, clr in rules[colour]) + 1

    return count_bags


def answer(path):
    with open(path) as f:
        rules = [
            r.split(" bags contain ") for r in f.read().strip().split("\n")
        ]

    count_bags = make_bag_counter(
        dict((r, extract_colours(s)) for r, s in rules)
    )

    return count_bags("shiny gold") - 1  # don't count the shiny gold one


if __name__ == "__main__":
    print(answer(sys.argv[1]))
