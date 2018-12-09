import re
import sys
from collections import deque


def answer(path):
    with open(path) as f:
        details = f.read()

    m = re.match(r"(\d+).*worth (\d+)", details)
    n_players = int(m.group(1))
    max_marble = int(m.group(2)) * 100

    marbles = deque([0])

    scores = [0] * n_players

    for i in range(1, max_marble + 1):
        if i % 23 == 0:
            marbles.rotate(7)
            removed = marbles.pop()
            scores[(i - 1) % n_players] += removed + i
            marbles.rotate(-1)
        else:
            marbles.rotate(-1)
            marbles.append(i)
    return max(scores)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
