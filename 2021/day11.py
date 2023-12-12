import sys
from itertools import chain, product


class Octopus:
    def __init__(self, energy_level, neighbours):
        self.energy_level = energy_level
        self.neighbours = neighbours
        self.n_flashes = 0
        self.last_flashed = -1

    def increment(self):
        self.energy_level += 1

    def reset(self):
        self.energy_level = 0
        self.n_flashes += 1


def get_neighbours(row, col, n_rows, n_cols):
    return [
        (row + i, col + j)
        for i, j in product([-1, 0, 1], [-1, 0, 1])
        if 0 <= row + i < n_rows
        and 0 <= col + j < n_cols
        and (i != 0 or j != 0)  # current location isn't a neighbour...
    ]


def load_data(path):
    def process_line(line):
        return [int(i) for i in line.strip()]

    with open(path) as f:
        energy_levels = [process_line(line) for line in f.readlines()]

    n_rows, n_cols = len(energy_levels), len(energy_levels[0])
    return [
        [
            Octopus(energy_level, get_neighbours(i, j, n_rows, n_cols))
            for j, energy_level in enumerate(row)
        ]
        for i, row in enumerate(energy_levels)
    ]


def evolve_single_step(octopuses, i):
    for octopus in chain(*octopuses):
        octopus.increment()

    def get_update_candidates():
        return [o for o in chain(*octopuses) if o.energy_level > 9]

    while len(to_update := get_update_candidates()) > 0:
        for octopus in to_update:
            for r, c in octopus.neighbours:
                o = octopuses[r][c]
                if o.last_flashed != i:
                    o.increment()
            octopus.reset()
            octopus.last_flashed = i


def part_1(octopuses, n_steps=100):
    for i in range(n_steps):
        evolve_single_step(octopuses, i)

    return sum(o.n_flashes for o in chain(*octopuses))


def part_2(octopuses):
    n_rows, n_cols = len(octopuses), len(octopuses[0])
    # octopuses has been evolved 100 times in first step
    i = 100
    while sum(o.energy_level == 0 for o in chain(*octopuses)) < n_rows * n_cols:
        evolve_single_step(octopuses, i)
        i += 1

    return i


if __name__ == "__main__":
    octopuses = load_data(sys.argv[1])
    print(f"Part 1: {part_1(octopuses)}")
    print(f"Part 2: {part_2(octopuses)}")
