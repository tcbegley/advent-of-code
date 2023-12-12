import sys
from collections import deque


def load_data(path):
    with open(path) as f:
        player1, player2 = [c.split("\n")[1:] for c in f.read().strip().split("\n\n")]

    player1 = [int(i) for i in player1]
    player2 = [int(i) for i in player2]

    return player1, player2


def calculate_score(winner):
    return sum(map(lambda ab: ab[0] * ab[1], enumerate(reversed(winner), start=1)))


def play_game(player1, player2):
    observed = set()
    while player1 and player2:
        state = (tuple(player1), tuple(player2))
        if state in observed:
            return 1, player1
        observed.add(state)

        p1 = player1.popleft()
        p2 = player2.popleft()

        if p1 <= len(player1) and p2 <= len(player2):
            winner, deck = play_game(
                deque(list(player1)[:p1]),
                deque(list(player2)[:p2]),
            )
            if winner == 1:
                player1.extend([p1, p2])
            else:
                player2.extend([p2, p1])
        elif p1 > p2:
            player1.extend([p1, p2])
        else:
            player2.extend([p2, p1])

    if player1:
        return 1, player1
    return 2, player2


def part_1(player1, player2):
    while player1 and player2:
        p1 = player1.popleft()
        p2 = player2.popleft()

        if p1 > p2:
            player1.extend([p1, p2])
        else:
            player2.extend([p2, p1])

    return calculate_score(player1 or player2)


def part_2(player1, player2):
    winner, deck = play_game(player1, player2)
    return calculate_score(deck)


if __name__ == "__main__":
    player1, player2 = load_data(sys.argv[1])
    print(f"Part 1: {part_1(deque(player1), deque(player2))}")
    print(f"Part 2: {part_2(deque(player1), deque(player2))}")
