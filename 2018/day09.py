import re
import sys
from collections import deque

NUMBER_PATTERN = re.compile(r"\d+")


def load_data(path):
    with open(path) as f:
        return map(int, NUMBER_PATTERN.findall(f.read()))


def play_game(n_players, points):
    circle = deque([0])
    scores = [0] * n_players

    for marble in range(1, points + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[(marble - 1) % n_players] += circle.popleft() + marble
        else:
            circle.rotate(-2)
            circle.appendleft(marble)

    return max(scores)


if __name__ == "__main__":
    n_players, points = load_data(sys.argv[1])
    print(f"Part 1: {play_game(n_players, points)}")
    print(f"Part 2: {play_game(n_players, points * 100)}")
