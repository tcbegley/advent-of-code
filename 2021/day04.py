import re
import sys

SPACE_PATTERN = re.compile(r"\s+")


class BingoCard:
    def __init__(self, card, size=5):
        self.size = size

        self.lookup = {}
        for i, row in enumerate(card):
            for j, number in enumerate(row):
                self.lookup[number] = (i, j)

        self.card = card
        self.seen = set()

    def __call__(self, number):
        try:
            self.seen.add(self.lookup[number])
        except KeyError:
            pass

        score = 0

        # check for win
        for i in range(self.size):
            if all((i, j) in self.seen for j in range(self.size)) or all(
                (j, i) in self.seen for j in range(self.size)
            ):
                score = max(score, self.get_score())

        return score * number

    def get_score(self):
        # score is sum of unmarked squares
        return sum(
            self.card[i][j]
            for i in range(self.size)
            for j in range(self.size)
            if (i, j) not in self.seen
        )


def load_data(path):
    with open(path) as f:
        numbers, *cards = f.read().strip().split("\n\n")

    def parse_card(card):
        return [
            [int(n) for n in SPACE_PATTERN.split(row.strip())]
            for row in card.split("\n")
        ]

    return [int(n) for n in numbers.split(",")], [parse_card(card) for card in cards]


def part_1(numbers, cards):
    cards = [BingoCard(card) for card in cards]

    for number in numbers:
        if (max_score := max(card(number) for card in cards)) > 0:
            return max_score


def part_2(numbers, cards):
    cards = [BingoCard(card) for card in cards]
    still_playing = {i for i in range(len(cards))}

    for number in numbers:
        for i, card in enumerate(cards):
            if i in still_playing and (score := card(number)) > 0:
                still_playing.remove(i)
                if not still_playing:
                    return score


if __name__ == "__main__":
    numbers, cards = load_data(sys.argv[1])
    print(f"Part 1: {part_1(numbers, cards)}")
    print(f"Part 2: {part_2(numbers, cards)}")
