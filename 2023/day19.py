import re
import sys
from collections import namedtuple
from dataclasses import dataclass

NUMBER_PATTERN = re.compile(r"\d+")
Part = namedtuple("Part", ["x", "m", "a", "s"])


@dataclass
class Node:
    name: str
    ranges: Part
    children: list["Node"] | None = None

    @property
    def combinations(self):
        return (
            (self.ranges.x[1] - self.ranges.x[0] + 1)
            * (self.ranges.m[1] - self.ranges.m[0] + 1)
            * (self.ranges.a[1] - self.ranges.a[0] + 1)
            * (self.ranges.s[1] - self.ranges.s[0] + 1)
        )


def extract_workflow(workflow):
    name, rules = workflow.removesuffix("}").split("{")
    rules = [extract_rule(rule) for rule in rules.split(",")]
    return name, rules


def extract_rule(rule):
    if ":" not in rule:
        return None, rule

    rule, dest = rule.split(":")
    return (rule[0], rule[1], int(rule[2:])), dest


def load_data(path):
    with open(path) as f:
        workflows, parts = f.read().strip().split("\n\n")

    parts = [
        Part(*map(int, NUMBER_PATTERN.findall(part))) for part in parts.split("\n")
    ]
    root = Node(
        name="in", ranges=Part(x=(1, 4_000), m=(1, 4_000), a=(1, 4_000), s=(1, 4_000))
    )
    root, count = dfs(root, dict(map(extract_workflow, workflows.split("\n"))))
    return root, count, parts


def apply_rule(parts, attr, op, value):
    interval = getattr(parts, attr)
    if op == ">":
        passing = (value + 1, interval[1])
        failing = (interval[0], value)
    else:
        passing = (interval[0], value - 1)
        failing = (value, interval[1])

    attrs = {k: getattr(parts, k) for k in "xmas"}

    if passing[0] <= passing[1]:
        passing = Part(**{**attrs, attr: passing})
    else:
        passing = None

    if failing[0] <= failing[1]:
        failing = Part(**{**attrs, attr: failing})
    else:
        failing = None

    return passing, failing


def dfs(root, workflows):
    children = []
    ranges = root.ranges
    count = 0

    for rule, dest in workflows[root.name]:
        if rule is None:
            passing = ranges
        else:
            passing, ranges = apply_rule(ranges, *rule)

        if dest in ("A", "R"):
            children.append(Node(name=dest, ranges=passing))
            count += children[-1].combinations * (dest == "A")
        else:
            node, delta = dfs(Node(name=dest, ranges=passing), workflows)
            children.append(node)
            count += delta

    root.children = children
    return root, count


def part_in_ranges(part, ranges):
    for attr in "xmas":
        value = getattr(part, attr)
        low, high = getattr(ranges, attr)
        if not low <= value <= high:
            return False
    return True


def check_part(root, part):
    if root.children is None:
        return root.name == "A"
    for child in root.children:
        if part_in_ranges(part, child.ranges):
            return check_part(child, part)


if __name__ == "__main__":
    root, count, parts = load_data(sys.argv[1])
    sum_of_ratings = sum(sum(part) for part in parts if check_part(root, part))
    print(f"Part 1: {sum_of_ratings}")
    print(f"Part 2: {count}")
