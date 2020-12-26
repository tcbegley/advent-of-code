import re
import sys

BLOCK = re.compile("|".join(f"{i}+" for i in range(10)))


def load_data(path):
    with open(path) as f:
        return f.read().strip()


def play_round(seq):
    blocks = BLOCK.findall(seq)
    return "".join(f"{len(block)}{block[0]}" for block in blocks)


def get_length(seq, iterations):
    for _ in range(iterations):
        seq = play_round(seq)
    return len(seq)


def part_1(seq):
    return get_length(seq, 40)


def part_2(seq):
    return get_length(seq, 50)


if __name__ == "__main__":
    seq = load_data(sys.argv[1])
    print(f"Part 1: {part_1(seq)}")
    print(f"Part 2: {part_2(seq)}")
