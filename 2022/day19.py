import re
import sys
from dataclasses import dataclass
from functools import cache, reduce

NUMBER_PATTERN = re.compile(r"\d+")


@dataclass(frozen=True)
class Blueprint:
    id: int
    o: int
    c: int
    ob: tuple[int, int]
    g: tuple[int, int]


def load_data(path):
    with open(path) as f:
        rows = [
            tuple(map(int, NUMBER_PATTERN.findall(row)))
            for row in f.read().strip().split("\n")
        ]

    return [
        Blueprint(id=id_, o=o, c=c, ob=(oo, oc), g=(go, gob))
        for id_, o, c, oo, oc, go, gob in rows
    ]


def triangle(n):
    return (n * (n - 1)) // 2


def max_geodes(bp: Blueprint, t: int = 24):
    max_ore = max(bp.o, bp.c, bp.ob[0], bp.g[0])
    max_clay = bp.ob[1]
    max_obsidian = bp.g[1]

    geodes = 0

    # use cache as a simple way to prune branches we've already traversed
    @cache
    def dfs(rem, o, c, ob, g, ro, rc, rob, rg):
        # since we're searching a tree to a fixed depth, DFS is a good choice
        # as we can prune branches that have no hope of exceeding the largest
        # number of geodes we've seen so far.
        nonlocal geodes
        if rem == 0:
            # update the largest number of geodes we've seen so far.
            geodes = max(geodes, g)
            return

        if g + rem * rg + triangle(rem - 1) < geodes:
            # if number of geodes + number that will be made by the end + the
            # max that could be made is less than the best number so far, then
            # we can prune this branch (triangle(rem-1) gives the number
            # of geodes we could make if we made a g robot every turn from
            # the current timestep until time ran out)
            return

        r = rem - 1
        if bp.g[0] <= o and bp.g[1] <= ob:
            dfs(
                r,
                min(o - bp.g[0] + ro, r * max_ore - (r - 1) * ro),
                min(c + rc, r * max_clay - (r - 1) * rc),
                min(ob - bp.g[1] + rob, r * max_obsidian - (r - 1) * rob),
                g + rg,
                ro,
                rc,
                rob,
                rg + 1,
            )
        if bp.ob[0] <= o and bp.ob[1] <= c and rob < max_obsidian:
            dfs(
                r,
                min(o - bp.ob[0] + ro, r * max_ore - (r - 1) * ro),
                min(c - bp.ob[1] + rc, r * max_clay - (r - 1) * rc),
                min(ob + rob, r * max_obsidian - (r - 1) * rob),
                g + rg,
                ro,
                rc,
                rob + 1,
                rg,
            )
        if bp.c <= o and rc < max_clay:
            dfs(
                r,
                min(o - bp.c + ro, r * max_ore - (r - 1) * ro),
                min(c + rc, r * max_clay - (r - 1) * rc),
                min(ob + rob, r * max_obsidian - (r - 1) * rob),
                g + rg,
                ro,
                rc + 1,
                rob,
                rg,
            )
        if bp.o <= o and ro < max_ore:
            dfs(
                r,
                min(o - bp.o + ro, r * max_ore - (r - 1) * ro),
                min(c + rc, r * max_clay - (r - 1) * rc),
                min(ob + rob, r * max_obsidian - (r - 1) * rob),
                g + rg,
                ro + 1,
                rc,
                rob,
                rg,
            )

        dfs(
            r,
            min(o + ro, r * max_ore - (r - 1) * ro),
            min(c + rc, r * max_clay - (r - 1) * rc),
            min(ob + rob, r * max_obsidian - (r - 1) * rob),
            g + rg,
            ro,
            rc,
            rob,
            rg,
        )

    dfs(t, 0, 0, 0, 0, 1, 0, 0, 0)
    return geodes


def part_1(blueprints):
    return sum(
        idx * geodes for idx, geodes in enumerate(map(max_geodes, blueprints), start=1)
    )


def part_2(blueprints):
    return reduce(
        lambda a, b: a * b, [max_geodes(bp, t=32) for bp in blueprints[:3]], 1
    )


if __name__ == "__main__":
    blueprints = load_data(sys.argv[1])
    print(f"Part 1: {part_1(blueprints)}")
    print(f"Part 2: {part_2(blueprints)}")
