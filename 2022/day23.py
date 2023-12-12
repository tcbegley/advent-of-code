import sys
from collections import Counter
from itertools import product

OFFSETS = [
    (((-1, 1), (0, 1), (1, 1)), (0, 1)),
    (((-1, -1), (0, -1), (1, -1)), (0, -1)),
    (((-1, -1), (-1, 0), (-1, 1)), (-1, 0)),
    (((1, -1), (1, 0), (1, 1)), (1, 0)),
]


def load_data(path):
    with open(path) as f:
        return {
            (x, y)
            for y, row in enumerate(reversed(f.read().strip().split("\n")))
            for x, char in enumerate(row)
            if char == "#"
        }


def get_neighbours(elf):
    for dx, dy in product((-1, 0, 1), (-1, 0, 1)):
        if dx == 0 and dy == 0:
            continue
        yield (elf[0] + dx, elf[1] + dy)


def add(elf, offset):
    (x, y), (dx, dy) = elf, offset
    return (x + dx, y + dy)


def evolve(elves, i):
    next_elves = {}
    for elf in elves:
        if all(nbr not in elves for nbr in get_neighbours(elf)):
            next_elves[elf] = elf
            continue
        for offsets, offset in OFFSETS[i:] + OFFSETS[:i]:
            if all(add(elf, o) not in elves for o in offsets):
                next_elves[elf] = add(elf, offset)
                break
        else:
            next_elves[elf] = elf

    counts = Counter(next_elves.values())
    return {next_elves[elf] if counts[next_elves[elf]] == 1 else elf for elf in elves}


def empty_space(elves):
    xs = [x for x, _ in elves]
    ys = [y for _, y in elves]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    return (maxx - minx + 1) * (maxy - miny + 1) - len(elves)


def part_1(elves):
    for i in range(10):
        elves = evolve(elves, i % 4)
    return empty_space(elves)


def part_2(elves):
    i = 0
    while True:
        next_elves = evolve(elves, i % 4)
        i += 1
        if next_elves == elves:
            break
        elves = next_elves
    return i


if __name__ == "__main__":
    elves = load_data(sys.argv[1])
    print(f"Part 1: {part_1(elves)}")
    print(f"Part 2: {part_2(elves)}")
