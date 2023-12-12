import sys
from functools import total_ordering
from itertools import chain


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None
        return left < right

    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]

    for lft, rgt in zip(left, right):
        if (res := compare(lft, rgt)) is not None:
            return res

    return compare(len(left), len(right))


@total_ordering
class Packet(list):
    # convenience class for sorting
    def __lt__(self, other):
        return compare(self, other)


def load_data(path):
    with open(path) as f:
        return [
            tuple(Packet(eval(x)) for x in pair.split("\n"))
            for pair in f.read().strip().split("\n\n")
        ]


def part_1(packets):
    return sum(
        i for i, (left, right) in enumerate(packets, start=1) if compare(left, right)
    )


def part_2(packets):
    p1, p2 = Packet([[2]]), Packet([[6]])
    packets = sorted(chain(*packets, (p1, p2)))
    return (packets.index(p1) + 1) * (packets.index(p2) + 1)


if __name__ == "__main__":
    packets = load_data(sys.argv[1])
    print(f"Part 1: {part_1(packets)}")
    print(f"Part 2: {part_2(packets)}")
