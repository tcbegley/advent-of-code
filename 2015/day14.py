import re
import sys

NUMBERS = re.compile(r"\d+")


class Reindeer:
    def __init__(self, speed, time, rest):
        self.speed = speed
        self.time = time
        self.T = time + rest

        self.loc = 0
        self.score = 0

    def advance(self, i):
        if (i % self.T) < self.time:
            self.loc += self.speed

    def increment_score(self):
        self.score += 1


def load_data(path):
    with open(path) as f:
        return [
            [int(i) for i in NUMBERS.findall(line)]
            for line in f.read().strip().split("\n")
        ]


def part_1(reindeer):
    reindeer = [Reindeer(*r) for r in reindeer]

    for i in range(2503):
        for r in reindeer:
            r.advance(i)

    return max(r.loc for r in reindeer)


def part_2(reindeer):
    reindeer = [Reindeer(*r) for r in reindeer]

    for i in range(2503):
        for r in reindeer:
            r.advance(i)

        max_loc = max(r.loc for r in reindeer)
        for r in reindeer:
            if r.loc == max_loc:
                r.increment_score()

    return max(r.score for r in reindeer)


if __name__ == "__main__":
    reindeer = load_data(sys.argv[1])
    print(f"Part 1: {part_1(reindeer)}")
    print(f"Part 2: {part_2(reindeer)}")
