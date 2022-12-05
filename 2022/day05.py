import re
import sys
from copy import deepcopy


def load_data(path):
    with open(path) as f:
        init_stacks, moves = f.read().split("\n\n")

    init_stacks = init_stacks.split("\n")
    n_stacks = len(init_stacks[-1].strip().split("   "))
    stacks = [[] for _ in range(n_stacks)]
    for row in reversed(init_stacks[:-1]):
        for i in range(n_stacks):
            idx = i * 4 + 1
            if idx >= len(row):
                break
            if (crate := row[idx]) != " ":
                stacks[i].append(crate)

    MOVE_PATTERN = re.compile(r"move (\d+) from (\d+) to (\d+)")
    moves = [
        tuple(map(int, MOVE_PATTERN.match(move).groups()))
        for move in moves.strip().split("\n")
    ]

    return stacks, moves


def part_1(stacks, moves):
    for n, src, dest in moves:
        for _ in range(n):
            stacks[dest - 1].append(stacks[src - 1].pop())

    return "".join(stack[-1] for stack in stacks)


def part_2(stacks, moves):
    for n, src, dest in moves:
        moving = stacks[src - 1][-n:]
        stacks[src - 1] = stacks[src - 1][:-n]
        stacks[dest - 1].extend(moving)

    return "".join(stack[-1] for stack in stacks)


if __name__ == "__main__":
    stacks, moves = load_data(sys.argv[1])
    # pass copy of stacks as they'll be mutated, messing up part 2
    print(f"Part 1: {part_1(deepcopy(stacks), moves)}")
    print(f"Part 2: {part_2(stacks, moves)}")
