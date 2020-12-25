import sys

MOD = 20201227


def load_data(path):
    with open(path) as f:
        return map(int, f.read().strip().split("\n"))


def part_1(door, card):
    value = 1
    card_loop_size = 0
    while value != card:
        value = (value * 7) % MOD
        card_loop_size += 1

    value = 1
    for _ in range(card_loop_size):
        value = (value * door) % MOD

    return value


if __name__ == "__main__":
    door, card = load_data(sys.argv[1])
    print(f"Part 1: {part_1(door, card)}")
