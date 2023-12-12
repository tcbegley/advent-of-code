import sys
from collections import defaultdict


def load_data(path):
    def process_line(line):
        start, end = line.strip().split(" -> ")
        start = [int(i) for i in start.split(",")]
        end = [int(i) for i in end.split(",")]
        return start, end

    with open(path) as f:
        return [process_line(line) for line in f.readlines()]


def get_range(start, end):
    if start <= end:
        return range(start, end + 1)
    return range(start, end - 1, -1)


def answer(lines, diagonals=False):
    covered = defaultdict(int)
    for start, end in lines:
        if start[0] == end[0]:
            for i in get_range(start[1], end[1]):
                covered[(start[0], i)] += 1
        elif start[1] == end[1]:
            for i in get_range(start[0], end[0]):
                covered[(i, start[1])] += 1
        elif diagonals:
            for i, j in zip(get_range(start[0], end[0]), get_range(start[1], end[1])):
                covered[(i, j)] += 1

    return sum(v >= 2 for v in covered.values())


def part_1(lines):
    return answer(lines)


def part_2(lines):
    return answer(lines, diagonals=True)


if __name__ == "__main__":
    lines = load_data(sys.argv[1])
    print(f"Part 1: {part_1(lines)}")
    print(f"Part 2: {part_2(lines)}")
