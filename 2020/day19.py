import re
import sys


def load_data(path):
    with open(path) as f:
        rules, messages = f.read().strip().split("\n\n")

    rules = dict(rule.split(": ") for rule in rules.split("\n"))
    return rules, messages.split("\n")


def build_regex(rule, rules):
    chunks = rule.split(" ")
    regex = ""
    for chunk in chunks:
        if chunk in rules:
            regex += build_regex(rules[chunk], rules)
        else:
            regex += chunk.strip('"')
    if "|" in regex:
        return f"({regex})"
    return regex


def count_matches(rules, messages):
    pattern = re.compile(build_regex(rules["0"], rules))
    count = 0
    for m in messages:
        if pattern.fullmatch(m):
            count += 1

    return count


def part_1(rules, messages):
    return count_matches(rules, messages)


def part_2(rules, messages):
    rules["8"] = "42 +"
    # this is horrible, but Python doesn't have recursive regex...
    # 5 is not necessarily the right number for all inputs
    rules["11"] = " | ".join([" ".join(["42"] * n + ["31"] * n) for n in range(1, 5)])
    return count_matches(rules, messages)


if __name__ == "__main__":
    rules, messages = load_data(sys.argv[1])
    print(f"Part 1: {part_1(rules, messages)}")
    print(f"Part 2: {part_2(rules, messages)}")
