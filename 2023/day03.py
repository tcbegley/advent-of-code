import sys
from dataclasses import dataclass
from string import digits


@dataclass
class Number:
    value: int
    digits: int
    start: int


def find_numbers(row: str):
    idx = 0
    while idx < len(row):
        if row[idx] in digits:
            i = idx
            while i < len(row) and row[i] in digits:
                i += 1
            yield Number(value=int(row[idx:i]), digits=i - idx, start=idx)
            idx = i
        idx += 1


def load_data(path):
    with open(path) as f:
        rows = f.read().strip().split("\n")

    number_lookup = {
        (r, num.start + c): num
        for r, row in enumerate(rows)
        for num in find_numbers(row)
        for c in range(num.digits)
    }

    symbols = {
        (r, c): char
        for r, row in enumerate(rows)
        for c, char in enumerate(row)
        if char not in digits + "."
    }

    return number_lookup, symbols


def get_neighbours(row, col):
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            yield (row + dr, col + dc)


def part_1(number_lookup, symbols):
    num_locs = set()
    for loc in symbols:
        num_locs |= set(
            (nbr[0], num.start)
            for nbr in get_neighbours(*loc)
            if (num := number_lookup.get(nbr)) is not None
        )

    return sum(number_lookup[loc].value for loc in num_locs)


def part_2(number_lookup, symbols):
    total = 0
    for loc, symbol in symbols.items():
        if symbol != "*":
            continue
        num_locs = set(
            (nbr[0], num.start)
            for nbr in get_neighbours(*loc)
            if (num := number_lookup.get(nbr)) is not None
        )
        if len(num_locs) == 2:
            loc1, loc2 = num_locs
            total += number_lookup[loc1].value * number_lookup[loc2].value

    return total


if __name__ == "__main__":
    number_lookup, symbols = load_data(sys.argv[1])
    print(f"Part 1: {part_1(number_lookup, symbols)}")
    print(f"Part 2: {part_2(number_lookup, symbols)}")
