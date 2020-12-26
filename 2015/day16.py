import sys

TARGET = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def load_data(path):
    with open(path) as f:
        return list(map(process_line, f.read().strip().split("\n")))


def process_line(line):
    _, line = line.split(": ", 1)
    items = dict(item.split(": ") for item in line.split(", "))
    return {k: int(v) for k, v in items.items()}


def part_1(sues):
    for i, sue in enumerate(sues, start=1):
        if all(TARGET[k] == v for k, v in sue.items()):
            return i


def part_2(sues):
    def check_value(k, v):
        if k in {"cats", "trees"}:
            return TARGET[k] < v
        elif k in {"pomeranians", "goldfish"}:
            return TARGET[k] > v
        else:
            return TARGET[k] == v

    for i, sue in enumerate(sues, start=1):
        if all(check_value(k, v) for k, v in sue.items()):
            return i


if __name__ == "__main__":
    sues = load_data(sys.argv[1])
    print(f"Print 1: {part_1(sues)}")
    print(f"Print 2: {part_2(sues)}")
