import sys

DIRS = {"U": (0, 1), "R": (1, 0), "D": (0, -1), "L": (-1, 0)}


def load_data(path):
    with open(path) as f:
        return [(row[0], int(row[2:])) for row in f.read().strip().split("\n")]


class Knot:
    def __init__(self):
        self.loc = (0, 0)
        self.head = (0, 0)

    def move(self, new_head):
        if (
            self.l1(new_head, self.loc) > 2
            or self.linf(new_head, self.loc) > 1
        ):
            self.loc = (
                self.step_towards(self.loc[0], new_head[0]),
                self.step_towards(self.loc[1], new_head[1]),
            )
        self.head = new_head

    @staticmethod
    def step_towards(a, b):
        # take a step from a in the direction of b
        if a < b:
            return a + 1
        elif a > b:
            return a - 1
        return a

    @staticmethod
    def l1(loc1, loc2):
        return abs(loc1[0] - loc2[0]) + abs(loc1[1] - loc2[1])

    @staticmethod
    def linf(loc1, loc2):
        return max(abs(loc1[0] - loc2[0]), abs(loc1[1] - loc2[1]))


def simulate(moves, chain_length=2):
    chain = [Knot() for _ in range(chain_length - 1)]
    head = (0, 0)
    visited = {chain[-1].loc}

    for d, count in moves:
        dx, dy = DIRS[d]
        for _ in range(count):
            loc = head = (head[0] + dx, head[1] + dy)
            for knot in chain:
                knot.move(loc)
                loc = knot.loc
            visited.add(loc)

    return len(visited)


def part_1(moves):
    return simulate(moves)


def part_2(moves):
    return simulate(moves, chain_length=10)


if __name__ == "__main__":
    moves = load_data(sys.argv[1])
    print(f"Part 1: {part_1(moves)}")
    print(f"Part 2: {part_2(moves)}")
