import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Rock:
    shape: set[tuple[int, int]]
    w: int
    h: int


ROCKS = [
    Rock(shape={(0, 0), (1, 0), (2, 0), (3, 0)}, w=4, h=1),  # minus
    Rock(shape={(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)}, w=3, h=3),  # plus
    Rock(shape={(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)}, w=3, h=3),  # corner
    Rock(shape={(0, 0), (0, 1), (0, 2), (0, 3)}, w=1, h=4),  # pipe
    Rock(shape={(0, 0), (0, 1), (1, 0), (1, 1)}, w=2, h=2),  # square
]


def load_data(path):
    with open(path) as f:
        return [1 if c == ">" else -1 for c in f.read().strip()]


def shift_rock(jet, rock, x):
    if jet == 1 and x + rock.w < 7:
        return x + 1
    elif jet == -1 and x > 0:
        return x - 1
    return x


def simulate(jets, n_rocks):
    n_jets = len(jets)

    chamber = set()
    jet_idx = rock_idx = 0
    max_ys = (0,) * 7
    height = 0

    seen = {}
    heights = []

    while rock_idx < n_rocks:
        rock = ROCKS[rock_idx % 5]
        x = 2
        y = height + 4

        while True:
            new_x = shift_rock(jets[jet_idx], rock, x)
            jet_idx = (jet_idx + 1) % n_jets

            if x != new_x and not (
                {(new_x + dx, y + dy) for dx, dy in rock.shape} & chamber
            ):
                x = new_x

            if y == 1 or {(x + dx, y + dy - 1) for dx, dy in rock.shape} & chamber:
                break

            y -= 1

        rock_location = {(x + dx, y + dy) for dx, dy in rock.shape}
        chamber.update(rock_location)
        max_ys = tuple(
            max([y for x, y in rock_location if x == i] + [max_y])
            for i, max_y in enumerate(max_ys)
        )
        height = max(max_ys)
        heights.append(height)
        rock_idx += 1

        state = (rock_idx % 5, jet_idx, tuple(h - height for h in max_ys))

        if state in seen:
            prev_height, prev_idx = seen[state]
            cycle_length = rock_idx - prev_idx
            height_delta = height - prev_height
            n_cycles, rem = divmod(n_rocks - prev_idx, cycle_length)
            return (
                prev_height
                + height_delta * n_cycles
                + heights[prev_idx + rem - 1]
                - heights[prev_idx - 1]
            )

        seen[state] = (height, rock_idx)

    return max(max_ys)


def part_1(jets):
    return simulate(jets, n_rocks=2022)


def part_2(jets):
    return simulate(jets, n_rocks=1_000_000_000_000)


if __name__ == "__main__":
    jets = load_data(sys.argv[1])
    print(f"Part 1: {part_1(jets)}")
    print(f"Part 2: {part_2(jets)}")
