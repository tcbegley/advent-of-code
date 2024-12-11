import sys
from functools import cache


def load_data(path):
    with open(path) as f:
        return [int(n) for n in f.read().strip().split(" ")]


@cache
def count(stone, blinks):
    if blinks == 0:
        return 1
    elif stone == 0:
        return count(1, blinks - 1)
    elif (n := len(stone_str := str(stone))) % 2 == 0:
        return count(int(stone_str[: n // 2]), blinks - 1) + count(
            int(stone_str[n // 2 :]), blinks - 1
        )
    return count(stone * 2024, blinks - 1)


def part_1(stones):
    return sum(count(stone, 25) for stone in stones)


def part_2(stones):
    return sum(count(stone, 75) for stone in stones)


if __name__ == "__main__":
    stones = load_data(sys.argv[1])
    print(f"Part 1: {part_1(stones)}")
    print(f"Part 2: {part_2(stones)}")
