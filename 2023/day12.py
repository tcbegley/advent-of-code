import sys
from functools import cache


def load_data(path):
    with open(path) as f:
        rows = [row.split(" ") for row in f.read().strip().split("\n")]

    return [(spring, tuple(map(int, counts.split(",")))) for spring, counts in rows]


@cache
def count_possibilities(springs, counts):
    if not counts:
        if any(c == "#" for c in springs):
            # combination is impossible
            return 0
        # one possibility: remaining springs are not functional
        return 1
    elif not springs:
        # no way to achieve positive counts with no springs remaining
        return 0

    if springs[0] == "?":
        # first spring is either functional, or it isn't. In former case replace with
        # functional and count again. In latter case discard
        return count_possibilities(f"#{springs[1:]}", counts) + count_possibilities(
            springs[1:], counts
        )

    if springs[0] == "#":
        count, *counts = counts
        # first spring is functional, so the first "count" springs must be alse, and
        # spring count + 1 (if it exists) must be broken
        if (
            len(springs) < count
            or any(c == "." for c in springs[:count])
            or (len(springs) > count and springs[count] == "#")
        ):
            return 0
        return count_possibilities(springs[count + 1 :], tuple(counts))
    else:
        # first char is ".", we can discard and move on
        return count_possibilities(springs[1:], counts)


def unfold(data):
    return [("?".join([springs] * 5), counts * 5) for springs, counts in data]


def part_1(data):
    return sum(count_possibilities(springs, counts) for springs, counts in data)


def part_2(data):
    return sum(count_possibilities(springs, counts) for springs, counts in unfold(data))


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
