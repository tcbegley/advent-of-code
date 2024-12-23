import sys
from itertools import combinations


def load_data(path):
    with open(path) as f:
        pairs = [line.split("-") for line in f.read().strip().split("\n")]

    computers = set()
    connections = {}
    for c1, c2 in pairs:
        computers.update([c1, c2])
        connections.setdefault(c1, set()).add(c2)
        connections.setdefault(c2, set()).add(c1)
    return list(computers), connections


def part_1(computers, connections):
    return sum(
        (
            a in connections[b]
            and a in connections[c]
            and b in connections[c]
            and any(name.startswith("t") for name in (a, b, c))
        )
        for a, b, c in combinations(computers, 3)
    )


def part_2(computers, connections):
    def backtrack(idx, included):
        if idx >= len(computers):
            yield included
        else:
            computer = computers[idx]
            if included.issubset(connections[computer]):
                yield from backtrack(idx + 1, {*included, computer})
            yield from backtrack(idx + 1, included)

    max_set = max(backtrack(0, set()), key=len)
    return ",".join(sorted(max_set))


if __name__ == "__main__":
    computers, connections = load_data(sys.argv[1])
    print(f"Part 1: {part_1(computers, connections)}")
    print(f"Part 2: {part_2(computers, connections)}")
