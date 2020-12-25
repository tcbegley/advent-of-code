import re
import sys
from string import ascii_lowercase

DOUBLE_PAIR = re.compile(r"([a-z]{2}).*(\1)")
SANDWICH = re.compile(r"([a-z]).(\1)")


def load_data(path):
    with open(path) as f:
        return f.read().strip().split("\n")


def is_nice_1(s):
    vowel_count = sum(s.count(c) for c in "aeiou") >= 3
    repeated_letter = any((2 * c in s for c in ascii_lowercase))
    no_disallowed = all((c not in s for c in ("ab", "cd", "pq", "xy")))
    return all((vowel_count, repeated_letter, no_disallowed))


def is_nice_2(s):
    return all([DOUBLE_PAIR.search(s), SANDWICH.search(s)])


def part_1(strings):
    return sum(map(is_nice_1, strings))


def part_2(key):
    return sum(map(is_nice_2, strings))


if __name__ == "__main__":
    strings = load_data(sys.argv[1])
    print(f"Part 1: {part_1(strings)}")
    print(f"Part 2: {part_2(strings)}")
