import re
import sys
from collections import namedtuple
from dataclasses import dataclass
from functools import partial
from operator import lt, gt

OPERATORS = {"<": lt, ">": gt}
NUMBER_PATTERN = re.compile(r"\d+")
Part = namedtuple("Part", ["x", "m", "a", "s"])


def extract_workflow(workflow, extract_rules):
    name, rules = workflow.removesuffix("}").split("{")
    rules = [extract_rule(rule) if extract_rules else rule for rule in rules.split(",")]
    return name, rules


def extract_part(part):
    return Part(*map(int, NUMBER_PATTERN.findall(part)))


def extract_rule(rule):
    if ":" not in rule:

        def check(part):
            return True

        return check, rule

    rule, dest = rule.split(":")
    attr = rule[0]
    op = rule[1]
    value = int(rule[2:])

    def check(part):
        return OPERATORS[op](getattr(part, attr), value)

    return check, dest


def load_data(path, extract_rules=True):
    with open(path) as f:
        workflows, parts = f.read().strip().split("\n\n")

    workflows = {
        name: rules
        for name, rules in map(
            partial(extract_workflow, extract_rules=extract_rules),
            workflows.split("\n"),
        )
    }
    parts = [extract_part(part) for part in parts.split("\n")]
    return workflows, parts


def process_part(workflows, part):
    workflow = "in"

    while workflow not in ("A", "R"):
        for rule, dest in workflows[workflow]:
            if rule(part):
                workflow = dest
                break

    return workflow


def part_1(workflows, parts):
    return sum(sum(part) for part in parts if process_part(workflows, part) == "A")


@dataclass
class Node:
    name: str
    ranges: Part
    children: list["Node"] | None


def part_2(workflows, parts):
    return workflows


if __name__ == "__main__":
    workflows, parts = load_data(sys.argv[1])
    print(f"Part 1: {part_1(workflows, parts)}")
    workflows, parts = load_data(sys.argv[1], extract_rules=False)
    print(f"Part 2: {part_2(workflows, parts)}")
