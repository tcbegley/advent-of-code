import sys
from functools import cache


def load_data(path):
    with open(path) as f:
        towels, designs = f.read().strip().split("\n\n")

    towel_lookup = {}
    for towel in towels.split(", "):
        towel_lookup.setdefault(towel[0], []).append(towel)
    designs = designs.split("\n")

    return towel_lookup, designs


def make_counter(towel_lookup):
    @cache
    def count(design):
        if len(design) == 0:
            return 1

        return sum(
            count(design.removeprefix(towel))
            for towel in towel_lookup.get(design[0], [])
            if design.startswith(towel)
        )

    return count


def part_1(towel_lookup, designs):
    count = make_counter(towel_lookup)
    return sum(count(design) > 0 for design in designs)


def part_2(towel_lookup, designs):
    count = make_counter(towel_lookup)
    return sum(count(design) for design in designs)


if __name__ == "__main__":
    towel_lookup, designs = load_data(sys.argv[1])
    print(f"Part 1: {part_1(towel_lookup, designs)}")
    print(f"Part 2: {part_2(towel_lookup, designs)}")
