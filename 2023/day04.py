import re
import sys

NUMBER = re.compile(r"\d+")


def process_row(row):
    row = row.split(":", 1)[1].strip()
    winning, ours = row.split("|")
    winning = set(map(int, NUMBER.findall(winning)))
    ours = set(map(int, NUMBER.findall(ours)))
    return winning, ours


def load_data(path):
    with open(path) as f:
        rows = f.read().strip().split("\n")

    return [process_row(row) for row in rows]


def part_1(data):
    return sum(
        2 ** (len(intersection) - 1)
        for winning, ours in data
        if (intersection := (winning & ours))
    )


def part_2(data):
    count = [1] * len(data)
    for i, (winning, ours) in enumerate(data):
        for j in range(i + 1, i + 1 + len(winning & ours)):
            if j < len(count):
                count[j] += count[i]

    return sum(count)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
