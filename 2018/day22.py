import sys
from functools import cache
from heapq import heappop, heappush


def load_data(path):
    with open(path) as f:
        depth, target = f.read().strip().split("\n")

    depth = int(depth.removeprefix("depth: "))
    target = tuple(map(int, target.removeprefix("target: ").split(",")))
    return depth, target


class Cave:
    def __init__(self, depth: int, target: tuple[int, int]) -> None:
        self.depth = depth
        self.target = target

    @cache
    def geological_index(self, loc) -> int:
        if loc == self.target:
            return 0

        x, y = loc
        if loc[0] == 0:
            return y * 48_271
        if y == 0:
            return x * 16_807
        return self.erosion_level((x, y - 1)) * self.erosion_level((x - 1, y))

    def erosion_level(self, loc):
        return (self.geological_index(loc) + self.depth) % 20_183

    def region_type(self, loc):
        return self.erosion_level(loc) % 3

    def __repr__(self):
        lookup = [".", "=", "|"]
        return r"\steps" + r"\steps".join(
            "".join(
                "M"
                if (x, y) == (0, 0)
                else "T"
                if (x, y) == self.target
                else lookup[self.erosion_level(x, y) % 3]
                for x in range(self.target[0] + 1)
            )
            for y in range(self.target[1] + 1)
        )


def l1(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def get_neighbours(loc):
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if 0 <= (nx := loc[0] + dx) and 0 <= (ny := loc[1] + dy):
            yield (nx, ny)


def part_1(depth, target):
    cave = Cave(depth, target)
    return sum(
        cave.region_type((x, y))
        for x in range(target[0] + 1)
        for y in range(target[1] + 1)
    )


def part_2(depth, target):
    cave = Cave(depth, target)

    start_state = ((0, 0), True, False)
    queue = [(l1((0, 0), target), 0, start_state)]
    seen = {start_state: 0}

    while queue:
        _, steps, state = heappop(queue)
        (loc, torch, climbing) = state

        if steps > seen.get(state, float("inf")):
            continue

        if loc == target and torch:
            return steps

        for nbr in get_neighbours(loc):
            region_type = cave.region_type(nbr)

            if (
                # can't enter a rocky region with nothing equipped
                (region_type != 0 or torch or climbing)
                # can't enter a wet region with torch equipped
                and (region_type != 1 or not torch)
                # can't enter narrow region with climbing equipment equipped
                and (region_type != 2 or not climbing)
            ):
                new_steps = steps + 1
                new_state = (nbr, torch, climbing)

                if new_steps < seen.get(new_state, float("inf")):
                    seen[new_state] = new_steps
                    heappush(queue, (new_steps + l1(nbr, target), new_steps, new_state))

        region_type = cave.region_type(loc)
        for t, c, el in [(False, False, 0), (True, False, 1), (False, True, 2)]:
            if region_type != el:
                new_steps = steps + 7
                new_state = (loc, t, c)
                if new_steps < seen.get(new_state, float("inf")):
                    seen[new_state] = new_steps
                    heappush(queue, (new_steps + l1(loc, target), new_steps, new_state))


if __name__ == "__main__":
    depth, target = load_data(sys.argv[1])
    print(f"Part 1: {part_1(depth, target)}")
    print(f"Part 2: {part_2(depth, target)}")
