import re
import sys
from collections import defaultdict


class Simulator:
    BOT_PATTERN = re.compile(
        r"bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)"
    )
    INPUT_PATTERN = re.compile(r"value (\d+) goes to bot (\d+)")

    def __init__(self, instructions):
        self.bots = {}
        self.outputs = defaultdict(list)

        self.instructions = instructions

        for instruction in self.instructions:
            if instruction.startswith("bot"):
                match = self.BOT_PATTERN.fullmatch(instruction)
                self.bots[int(match.group(1))] = {
                    "chips": [],
                    "low": (match.group(2), int(match.group(3))),
                    "high": (match.group(4), int(match.group(5))),
                }

    def simulate(self):
        for instruction in self.instructions:
            if instruction.startswith("value"):
                match = self.INPUT_PATTERN.fullmatch(instruction)
                self.place(int(match.group(2)), int(match.group(1)))

    def place(self, idx, chip):
        self.bots[idx]["chips"].append(chip)
        if len(self.bots[idx]["chips"]) == 2:
            low_type, low = self.bots[idx]["low"]
            high_type, high = self.bots[idx]["high"]

            if low_type == "output":
                self.outputs[low].append(min(self.bots[idx]["chips"]))
            else:
                self.place(low, min(self.bots[idx]["chips"]))

            if high_type == "output":
                self.outputs[high].append(max(self.bots[idx]["chips"]))
            else:
                self.place(high, max(self.bots[idx]["chips"]))


def load_data(path):
    with open(path) as f:
        return [line.strip() for line in f.readlines()]


def part_1(simulator):
    for bot_id, bot_details in simulator.bots.items():
        if set(bot_details["chips"]) == {17, 61}:
            return bot_id


def part_2(simulator):
    return (
        simulator.outputs[0][0]
        * simulator.outputs[1][0]
        * simulator.outputs[2][0]
    )


if __name__ == "__main__":
    instructions = load_data(sys.argv[1])
    simulator = Simulator(instructions)
    simulator.simulate()
    print(f"Part 1: {part_1(simulator)}")
    print(f"Part 2: {part_2(simulator)}")
