import sys


def load_data(path):
    with open(path) as f:
        return [int(i) for i in f.readlines()]


def part_1(steps):
    return sum(steps)


def part_2(steps):
    i, n = 0, len(steps)
    total = 0
    seen = set()

    while True:
        if total in seen:
            return total
        seen.add(total)
        total += steps[i]
        i = (i + 1) % n


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
