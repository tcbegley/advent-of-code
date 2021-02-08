import sys
from collections import Counter


def load_data(path):
    with open(path) as f:
        return f.read().strip().split("\n")


def part_1(messages):
    n = len(messages[0])
    return "".join(
        Counter(m[i] for m in messages).most_common(1)[0][0] for i in range(n)
    )


def part_2(messages):
    n = len(messages[0])
    return "".join(
        Counter(m[i] for m in messages).most_common()[-1][0] for i in range(n)
    )


if __name__ == "__main__":
    messages = load_data(sys.argv[1])
    print(f"Part 1: {part_1(messages)}")
    print(f"Part 2: {part_2(messages)}")
