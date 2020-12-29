import sys


def load_data(path):
    with open(path) as f:
        return [int(x.strip()) for x in f.readlines()]


def part_1(steps):
    n, count, i = len(steps), 0, 0

    while 0 <= i < n:
        steps[i], i, count = steps[i] + 1, steps[i] + i, count + 1

    return count


def part_2(steps):
    n, count, i = len(steps), 0, 0

    while 0 <= i < n:
        if steps[i] >= 3:
            steps[i], i = steps[i] - 1, steps[i] + i
        else:
            steps[i], i = steps[i] + 1, steps[i] + i
        count += 1

    return count


if __name__ == "__main__":
    steps = load_data(sys.argv[1])
    print(f"Part 1: {part_1(steps[:])}")
    print(f"Part 2: {part_2(steps)}")
