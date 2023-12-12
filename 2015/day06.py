import re
import sys
from collections import defaultdict

from tqdm.auto import tqdm

PATTERN = re.compile(r"([\w ]+) (\d+),(\d+) through (\d+),(\d+)")


def load_data(path):
    with open(path) as f:
        return [
            ((g := m.group)(1), int(g(2)), int(g(3)), int(g(4)), int(g(5)))
            for m in map(PATTERN.fullmatch, f.read().strip().split("\n"))
        ]


def setup_lights(instructions, toggle, turn_on, turn_off, lights):
    for action, x_start, y_start, x_end, y_end in tqdm(instructions, leave=False):
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                if action == "toggle":
                    lights[(x, y)] = toggle(lights[(x, y)])
                elif action == "turn on":
                    lights[(x, y)] = turn_on(lights[(x, y)])
                elif action == "turn off":
                    lights[(x, y)] = turn_off(lights[(x, y)])

    return lights


def part_1(instructions):
    initial_lights = defaultdict(lambda: False)
    lights = setup_lights(
        instructions,
        toggle=lambda x: not x,
        turn_on=lambda x: True,
        turn_off=lambda x: False,
        lights=initial_lights,
    )
    return sum(lights.values())


def part_2(instructions):
    initial_lights = defaultdict(lambda: 0)
    lights = setup_lights(
        instructions,
        toggle=lambda x: x + 2,
        turn_on=lambda x: x + 1,
        turn_off=lambda x: max(x - 1, 0),
        lights=initial_lights,
    )
    return sum(lights.values())


if __name__ == "__main__":
    instructions = load_data(sys.argv[1])
    print(f"Part 1: {part_1(instructions)}")
    print(f"Part 2: {part_2(instructions)}")
