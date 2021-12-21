import sys
from dataclasses import dataclass
from functools import cache

MULTIPLIER = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


@dataclass
class Player:
    position: int
    score: int = 0


def load_data(path):
    def process_line(line):
        return int(line.strip().rsplit(" ", 1)[1])

    with open(path) as f:
        return [process_line(line) for line in f.readlines()]


def part_1(data):
    p1_loc, p2_loc = data
    p1_score, p2_score = 0, 0
    p1s_turn = True
    rolls = 0

    while p1_score < 1000 and p2_score < 1000:
        advance = ((rolls) % 100 + (rolls + 1) % 100 + (rolls + 2) % 100) + 3
        rolls += 3
        if p1s_turn:
            p1_loc = (p1_loc - 1 + advance) % 10 + 1
            p1_score += p1_loc
        else:
            p2_loc = (p2_loc - 1 + advance) % 10 + 1
            p2_score += p2_loc
        p1s_turn = not p1s_turn

    return min(p1_score, p2_score) * rolls


@cache
def count_wins(p1_loc, p2_loc, p1_score, p2_score, p1s_turn):
    if p1_score >= 21:
        return 1, 0
    elif p2_score >= 21:
        return 0, 1

    wins = (0, 0)
    for advance, weight in MULTIPLIER.items():
        if p1s_turn:
            p1_new_loc = (p1_loc - 1 + advance) % 10 + 1
            p1_new_score = p1_score + p1_new_loc
            p2_new_loc, p2_new_score = p2_loc, p2_score
        else:
            p2_new_loc = (p2_loc - 1 + advance) % 10 + 1
            p2_new_score = p2_score + p2_new_loc
            p1_new_loc, p1_new_score = p1_loc, p1_score

        new_wins = count_wins(
            p1_new_loc, p2_new_loc, p1_new_score, p2_new_score, not p1s_turn
        )
        wins = (
            wins[0] + new_wins[0] * weight,
            wins[1] + new_wins[1] * weight,
        )
    return wins


def part_2(data):
    return max(count_wins(data[0], data[1], 0, 0, True))


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
