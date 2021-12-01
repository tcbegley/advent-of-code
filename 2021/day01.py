import sys


def triplewise(sequence):
    # zip terminates when shortest sequence is exhausted
    return zip(sequence, sequence[1:], sequence[2:])


def load_data(path):
    with open(path) as f:
        return [int(n) for n in f.read().strip().split("\n")]


def part_1(depths):
    return sum(d2 > d1 for d2, d1 in zip(depths[1:], depths))


def part_2(depths):
    return sum(
        sum(t2) > sum(t1)
        for t2, t1 in zip(triplewise(depths[1:]), triplewise(depths))
    )


if __name__ == "__main__":
    depths = load_data(sys.argv[1])
    print(f"Part 1: {part_1(depths)}")
    print(f"Part 2: {part_2(depths)}")
