import sys
from collections import namedtuple
from itertools import chain, combinations, product

Fighter = namedtuple("Fighter", ["hp", "damage", "armour"])

WEAPONS = [(8, 4, 0), (10, 5, 0), (25, 6, 0), (40, 7, 0), (74, 8, 0)]
ARMOUR = [(13, 0, 1), (31, 0, 2), (53, 0, 3), (75, 0, 4), (102, 0, 5)]
RINGS = [
    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3),
]


def load_data(path):
    with open(path) as f:
        return Fighter(
            *[
                int(line.split(": ")[1])
                for line in f.read().strip().split("\n")
            ]
        )


def gen_items():
    return (
        tuple(chain.from_iterable(x))
        for x in product(
            combinations(WEAPONS, 1),
            chain(combinations(ARMOUR, 0), combinations(ARMOUR, 1)),
            chain.from_iterable(combinations(RINGS, i) for i in range(3)),
        )
    )


def n_turns(player1, player2):
    return (player2.hp - 1) // max(player1.damage - player2.armour, 1) + 1


def fight(player, boss):
    return n_turns(player, boss) <= n_turns(boss, player)


def part_1(boss):
    items = sorted(
        gen_items(), key=lambda items: sum(item[0] for item in items)
    )
    for item_set in items:
        player = Fighter(
            100, sum(i[1] for i in item_set), sum(i[2] for i in item_set)
        )
        if fight(player, boss):
            return sum(i[0] for i in item_set)


def part_2(boss):
    items = sorted(
        gen_items(),
        key=lambda items: sum(item[0] for item in items),
        reverse=True,
    )
    for item_set in items:
        player = Fighter(
            100, sum(i[1] for i in item_set), sum(i[2] for i in item_set)
        )
        if not fight(player, boss):
            return sum(i[0] for i in item_set)


if __name__ == "__main__":
    boss = load_data(sys.argv[1])
    print(f"Part 1: {part_1(boss)}")
    print(f"Part 2: {part_2(boss)}")
