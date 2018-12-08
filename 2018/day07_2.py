import re
import sys
from string import ascii_uppercase


class Elf:
    TIMES = {l: i + 61 for i, l in enumerate(ascii_uppercase)}

    def __init__(self):
        self.available = 0
        self.task = None

    def assign(self, task, time):
        self.task = task
        self.available = time + self.TIMES[task]


def answer(path):
    with open(path) as f:
        instructions_raw = f.read().strip().split("\n")
    instructions = []
    for i in instructions_raw:
        m = re.match("Step ([A-Z]).*step ([A-Z])", i)
        instructions.append((m.group(1), m.group(2)))

    steps = []
    for i in instructions:
        steps.extend(i)

    dependencies = {s: set() for s in set(steps)}

    for i in instructions:
        dependencies[i[1]].add(i[0])

    elves = [Elf() for _ in range(5)]
    time = 0
    while dependencies:
        # loop over workers once to update completed tasks
        for e in elves:
            if e.available <= time:
                for v in dependencies.values():
                    if e.task in v:
                        v.remove(e.task)
        # loop a second time to assign new tasks
        for e in elves:
            if e.available <= time:
                candidates = [
                    k for k, v in dependencies.items() if len(v) == 0
                ]
                if candidates:
                    i = min(candidates)
                    e.assign(i, time)
                    dependencies.pop(i)
        time += 1

    # the completion time is also the time the final worker becomes available
    return max(e.available for e in elves)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
