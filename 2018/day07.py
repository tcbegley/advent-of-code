import re
import sys


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

    out = ""
    while dependencies:
        i = min([k for k, v in dependencies.items() if len(v) == 0])
        out += i
        dependencies.pop(i)
        for v in dependencies.values():
            if i in v:
                v.remove(i)

    return out


if __name__ == "__main__":
    print(answer(sys.argv[1]))
