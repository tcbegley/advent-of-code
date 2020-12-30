import re
import sys


def load_data(path):
    with open(path) as f:
        stream = f.read().strip()
    return re.sub(r"!.", "", stream)


def parse(stream):
    n, left = 0, 1
    for right in range(len(stream)):
        if stream[right] == "{":
            n += 1
        elif stream[right] == "}":
            n -= 1
        if n == 0:
            yield stream[left:right]
            left = right + 2


def score(stream, n):
    return n + sum([score(x, n + 1) for x in parse(stream)])


def part_1(stream):
    stream = re.sub(r"<[^>]*>", "", stream)
    stream = re.sub(r"[^{}]", "", stream)
    return score(stream, 0)


def part_2(stream):
    garbage = re.findall(r"<([^>]*)>", stream)
    return len("".join(garbage))


if __name__ == "__main__":
    stream = load_data(sys.argv[1])
    print(f"Part 1: {part_1(stream)}")
    print(f"Part 2: {part_2(stream)}")
