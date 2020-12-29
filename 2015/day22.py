import sys
from collections import deque, namedtuple

Wizard = namedtuple("Wizard", ["hp", "armour", "mana"])
Boss = namedtuple("Boss", ["hp", "damage"])
Effects = namedtuple("Effects", ["shield", "poison", "recharge"])
Game = namedtuple("Game", ["wizard", "boss", "effects", "mana_spent"])


def apply_effects(game):
    wizard = list(game.wizard)
    wizard[1] = 7 if game.effects.shield else 0
    if game.effects.recharge > 0:
        wizard[2] += 101

    boss = list(game.boss)
    if game.effects.poison > 0:
        boss = Boss(game.boss[0] - 3, game.boss[1])

    wizard = Wizard(*wizard)
    boss = Boss(*boss)
    effects = Effects(*[max(0, e - 1) for e in game.effects])
    return Game(wizard, boss, effects, game.mana_spent)


def magic_missile(game):
    wizard = Wizard(game.wizard.hp, game.wizard.armour, game.wizard.mana - 53)
    boss = Boss(game.boss.hp - 4, game.boss.damage)
    return Game(wizard, boss, game.effects, game.mana_spent + 53)


def drain(game):
    wizard = Wizard(
        game.wizard.hp + 2, game.wizard.armour, game.wizard.mana - 73
    )
    boss = Boss(game.boss.hp - 2, game.boss.damage)
    return Game(wizard, boss, game.effects, game.mana_spent + 73)


def shield(game):
    wizard = Wizard(game.wizard.hp, game.wizard.armour, game.wizard.mana - 113)
    effects = Effects(6, game.effects.poison, game.effects.recharge)
    return Game(wizard, game.boss, effects, game.mana_spent + 113)


def poison(game):
    wizard = Wizard(game.wizard.hp, game.wizard.armour, game.wizard.mana - 173)
    effects = Effects(game.effects.shield, 6, game.effects.recharge)
    return Game(wizard, game.boss, effects, game.mana_spent + 173)


def recharge(game):
    wizard = Wizard(game.wizard.hp, game.wizard.armour, game.wizard.mana - 229)
    effects = Effects(game.effects.shield, game.effects.poison, 5)
    return Game(wizard, game.boss, effects, game.mana_spent + 229)


SPELLS = [
    (magic_missile, 53),
    (drain, 73),
    (shield, 113),
    (poison, 173),
    (recharge, 229),
]


def boss_turn(game):
    return Game(
        Wizard(
            game.wizard.hp - max(game.boss.damage - game.wizard.armour, 1),
            *game.wizard[1:],
        ),
        game.boss,
        game.effects,
        game.mana_spent,
    )


def cast_spell(game, spell, hard_mode):
    if hard_mode:
        game = Game(
            Wizard(game.wizard.hp - 1, *game.wizard[1:]),
            game.boss,
            game.effects,
            game.mana_spent,
        )
        if game.wizard.hp <= 0:
            return float("inf")

    game = apply_effects(game)
    if game.boss.hp <= 0:
        return game.mana_spent

    game = spell(game)
    if game.boss.hp <= 0:
        return game.mana_spent

    game = apply_effects(game)
    if game.boss.hp <= 0:
        return game.mana_spent

    game = boss_turn(game)
    if game.wizard.hp <= 0:
        return float("inf")

    return game


def breadth_first_search(b, hard_mode=False):
    w = Wizard(50, 0, 500)
    b = Boss(*b)
    e = Effects(0, 0, 0)
    game = Game(w, b, e, 0)

    queue = deque([game])
    best_expenditure = float("inf")

    while queue:
        game = queue.popleft()

        for spell, cost in SPELLS:
            if (
                cost > game.wizard.mana
                or (spell == shield and game.effects.shield > 1)
                or (spell == poison and game.effects.poison > 1)
                or (spell == recharge and game.effects.recharge > 1)
            ):
                continue
            res = cast_spell(game, spell, hard_mode)
            if isinstance(res, Game):
                if res.mana_spent < best_expenditure:
                    queue.append(res)
            elif res < best_expenditure:
                best_expenditure = res

    return best_expenditure


def load_data(path):
    with open(path) as f:
        return [
            int(line.split(": ")[1]) for line in f.read().strip().split("\n")
        ]


def part_1(b):
    return breadth_first_search(b)


def part_2(b):
    return breadth_first_search(b, True)


if __name__ == "__main__":
    b = load_data(sys.argv[1])
    print(f"Part 1: {part_1(b)}")
    print(f"Part 2: {part_2(b)}")
