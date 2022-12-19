import re
import sys
from dataclasses import dataclass
from functools import cache

NUMBER_PATTERN = re.compile(r"\d+")


@dataclass
class Blueprint:
    id: int
    o: int
    c: int
    ob: tuple[int, int]
    geode: tuple[int, int]


def load_data(path):
    with open(path) as f:
        rows = [
            tuple(map(int, NUMBER_PATTERN.findall(row)))
            for row in f.read().strip().split("\n")
        ]

    return [
        Blueprint(id=id_, o=o, c=c, ob=(oo, oc), geode=(go, gob))
        for id_, o, c, oo, oc, go, gob in rows
    ]


def max_geodes(bp: Blueprint):
    @cache
    def geodes(r, o, c, ob, orr, cr, obr):
        if r == 0:
            return 0

        n_geodes = 0
        if o >= bp.o:
            n_geodes = max(
                n_geodes,
                geodes(
                    r - 1, o - bp.o + orr, c + cr, ob + obr, orr + 1, cr, obr
                ),
            )
        if o >= bp.c:
            n_geodes = max(
                n_geodes,
                geodes(
                    r - 1,
                    o - bp.c + orr,
                    c + cr,
                    ob + obr,
                    orr,
                    cr + 1,
                    obr,
                ),
            )
        if o >= bp.ob[0] and c >= bp.ob[1]:
            n_geodes = max(
                n_geodes,
                geodes(
                    r - 1,
                    o - bp.ob[0] + orr,
                    c - bp.ob[1] + cr,
                    ob + obr,
                    orr,
                    cr,
                    obr + 1,
                ),
            )
        if o >= bp.geode[0] and ob >= bp.geode[1]:
            n_geodes = max(
                n_geodes,
                geodes(
                    r - 1,
                    o - bp.geode[0] + orr,
                    c + cr,
                    ob - bp.geode[1] + obr,
                    orr,
                    cr,
                    obr,
                )
                + r,
            )
        return max(
            n_geodes,
            geodes(r - 1, o + orr, c + cr, ob + obr, orr, cr, obr),
        )

    return geodes(24, 0, 0, 0, 1, 0, 0)


def part_1(blueprints):
    return max(max_geodes(bp) for bp in blueprints)


def part_2(blueprints):
    pass


if __name__ == "__main__":
    blueprints = load_data(sys.argv[1])
    print(f"Part 1: {part_1(blueprints)}")
    print(f"Part 2: {part_2(blueprints)}")
