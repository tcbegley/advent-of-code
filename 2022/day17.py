import sys
from collections import namedtuple
from dataclasses import dataclass

STEPS = 1_000_000_000_000

State = namedtuple("State", ["jet_idx", "rock", "heights"])


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


def print_chamber(chamber):
    height = max(y for x, y in chamber)
    print(
        "\n".join(
            [
                "".join("#" if (x, y) in chamber else "." for x in range(7))
                for y in range(height + 2, 0, -1)
            ]
            + ["-" * 7]
        ),
        end="\n" * 3,
    )


def part_1(jets):
    chamber = set()
    heights = (0,) * 7
    jet_idx = 0
    n_jets = len(jets)

    for rock_idx in range(2022):
        rock = ROCKS[rock_idx % 5]
        x = 2
        y = max(heights) + 4

        while True:
            new_x = shift_rock(jets[jet_idx], rock, x)

            if x != new_x and not (
                {(new_x + dx, y + dy) for dx, dy in rock.shape} & chamber
            ):
                x = new_x

            jet_idx = (jet_idx + 1) % n_jets
            next_rock = {(x + dx, y + dy - 1) for dx, dy in rock.shape}
            if y == 1 or next_rock & chamber:
                break
            y -= 1

        rock_location = {(x + dx, y + dy) for dx, dy in rock.shape}
        chamber.update(rock_location)
        heights = tuple(
            max([y for x_, y in rock_location if x_ == x] + [h])
            for x, h in enumerate(heights)
        )

    return max(heights)


def part_2(jets):
    chamber = set()
    heights = (0,) * 7
    height = 0
    jet_idx = 0
    n_jets = len(jets)
    rock_idx = 0

    seen = {}
    change = []

    while rock_idx < STEPS:
        rock = ROCKS[rock_idx % 5]
        x = 2
        y = max(heights) + 4

        while True:
            new_x = shift_rock(jets[jet_idx], rock, x)

            if x != new_x and not (
                {(new_x + dx, y + dy) for dx, dy in rock.shape} & chamber
            ):
                x = new_x

            jet_idx = (jet_idx + 1) % n_jets
            next_rock = {(x + dx, y + dy - 1) for dx, dy in rock.shape}
            if y == 1 or next_rock & chamber:
                break
            y -= 1

        rock_location = {(x + dx, y + dy) for dx, dy in rock.shape}
        chamber.update(rock_location)
        heights = tuple(
            max([y for x_, y in rock_location if x_ == x] + [h])
            for x, h in enumerate(heights)
        )
        change.append(max(heights) - height)
        height = max(heights)
        rock_idx += 1

        state = (rock_idx % 5, jet_idx, tuple(h - height for h in heights))

        if state in seen:
            prev_height, prev_idx = seen[state]
            cycle_length = rock_idx - prev_idx
            height_delta = height - prev_height
            n_cycles, rem = divmod(STEPS - prev_idx, cycle_length)
            return (
                prev_height
                + height_delta * n_cycles
                + sum(change[prev_idx : prev_idx + rem])
            )

        seen[state] = (height, rock_idx)

    return max(heights)


if __name__ == "__main__":
    jets = load_data(sys.argv[1])
    print(f"Part 1: {part_1(jets)}")
    print(f"Part 2: {part_2(jets)}")
