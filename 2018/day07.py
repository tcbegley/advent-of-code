import re
import sys
from collections import defaultdict
from string import ascii_uppercase

DATA_PATTERN = re.compile(r"Step ([A-Z]).*step ([A-Z])")
TIMES = {letter: i + 60 for i, letter in enumerate(ascii_uppercase, start=1)}


def load_data(path):
    with open(path) as f:
        orderings = [
            DATA_PATTERN.match(row).groups()
            for row in f.read().strip().split("\n")
        ]

    dependencies = {}
    for node, descendant in orderings:
        dependencies.setdefault(descendant, set()).add(node)
        dependencies.setdefault(node, set())

    return dependencies


def solve(dependencies):
    available = 5
    finishing = defaultdict(list)
    time = 0
    order = []

    while dependencies:
        for task in finishing[time]:
            # remove completed tasks from dependencies
            available += 1
            for v in dependencies.values():
                if task in v:
                    v.remove(task)
        while available > 0:
            # all tasks that could be started
            tasks = [
                task for task, deps in dependencies.items() if len(deps) == 0
            ]
            if tasks:
                # start with first alphabetically
                task = min(tasks)
                order.append(task)
                # keep track of when task will finish
                finishing[time + TIMES[task]] = task
                # decrement available workers
                available -= 1
                dependencies.pop(task)
            else:
                # no tasks available, go to next time step
                break
        time += 1

    return order, max(finishing)


if __name__ == "__main__":
    dependencies = load_data(sys.argv[1])
    order, time_taken = solve(dependencies)
    print(f"Part 1: {''.join(order)}")
    print(f"Part 2: {time_taken}")
