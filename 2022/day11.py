import re
import sys
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from typing import Optional

INT_PATTERN = re.compile(r"\d+")


@dataclass
class Monkey:
    items: list[int]
    multiply: bool
    arg: Optional[int]
    divisor: int
    true_monkey: int
    false_monkey: int
    num_inspections: int = 0


def load_data(path):
    with open(path) as f:
        blocks = f.read().strip().split("\n\n")

    monkeys = []
    for block in blocks:
        lines = block.split("\n")
        items = list(map(int, INT_PATTERN.findall(lines[1])))
        _, arg = lines[2].rsplit(" ", 1)
        try:
            arg = int(arg)
        except ValueError:
            arg = None
        monkeys.append(
            Monkey(
                items=items,
                multiply="*" in block,
                arg=arg,
                divisor=int(lines[3].rsplit(" ", 1)[1]),
                true_monkey=int(lines[4].rsplit(" ", 1)[1]),
                false_monkey=int(lines[5].rsplit(" ", 1)[1]),
            )
        )
    return monkeys


def simulate_round(monkeys, item_hook):
    for monkey in monkeys:
        for item in monkey.items:
            monkey.num_inspections += 1
            if monkey.multiply:
                item *= monkey.arg if monkey.arg is not None else item
            else:
                item += monkey.arg if monkey.arg is not None else item
            item = item_hook(item)
            if item % monkey.divisor == 0:
                monkeys[monkey.true_monkey].items.append(item)
            else:
                monkeys[monkey.false_monkey].items.append(item)
            monkey.items = []
    return monkeys


def simulate(monkeys, n_rounds, item_hook):
    for _ in range(n_rounds):
        monkeys = simulate_round(monkeys, item_hook)
    activity = sorted([monkey.num_inspections for monkey in monkeys], reverse=True)
    return activity[0] * activity[1]


def part_1(monkeys):
    return simulate(monkeys, 20, lambda item: item // 3)


def part_2(monkeys):
    # we can mod out factors of a common multiple of the divisor tests without
    # changing the outcome of any individual test.
    common_divisor = reduce(lambda a, b: a * b, [m.divisor for m in monkeys])
    return simulate(monkeys, 10_000, lambda item: item % common_divisor)


if __name__ == "__main__":
    monkeys = load_data(sys.argv[1])
    print(f"Part 1: {part_1(deepcopy(monkeys))}")
    print(f"Part 2: {part_2(monkeys)}")
