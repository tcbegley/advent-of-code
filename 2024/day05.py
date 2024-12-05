import sys
from graphlib import TopologicalSorter


def load_data(path):
    with open(path) as f:
        rules, updates = f.read().strip().split("\n\n")
    rules = {tuple(int(n) for n in row.split("|")) for row in rules.split("\n")}
    updates = [[int(n) for n in row.split(",")] for row in updates.split("\n")]

    return rules, updates


def part_1(rules, updates):
    return sum(
        update[len(update) // 2]
        for update in updates
        if not any(
            (right, left) in rules
            for i, left in enumerate(update)
            for right in update[i:]
        )
    )


def sort(update, rules):
    # have to filter rules before topological sort because the full collection of rules
    # contains a cycle!
    values = set(update)
    graph = {}
    for left, right in rules:
        if left in values and right in values:
            graph.setdefault(right, set()).add(left)

    return list(TopologicalSorter(graph).static_order())


def part_2(rules, updates):
    return sum(
        sort(update, rules)[len(update) // 2]
        for update in updates
        if any(
            (right, left) in rules
            for i, left in enumerate(update)
            for right in update[i:]
        )
    )


if __name__ == "__main__":
    rules, updates = load_data(sys.argv[1])
    print(f"Part 1: {part_1(rules, updates)}")
    print(f"Part 2: {part_2(rules, updates)}")
