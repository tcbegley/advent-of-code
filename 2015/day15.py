import re
import sys
from functools import reduce

from tqdm.auto import tqdm

NUMBERS = re.compile(r"-?\d+")


def load_data(path):
    with open(path) as f:
        return [
            [int(i) for i in NUMBERS.findall(line)]
            for line in f.read().strip().split("\n")
        ]


def make_scorer(ingredients):
    def score(*quantities):
        scores = [
            max(sum(q * ing[i] for q, ing in zip(quantities, ingredients)), 0)
            for i in range(5)
        ]
        return reduce(lambda a, b: a * b, scores[:4]), scores[4]

    return score


def get_scores(ingredients):
    score = make_scorer(ingredients)

    return [
        score(spr, pb, f, sug)
        for spr in tqdm(range(101), leave=False)
        for pb in range(101 - spr)
        for f in range(101 - spr - pb)
        for sug in range(101 - spr - pb - f)
    ]


def part_1(scores):
    return max(s for s, _ in scores)


def part_2(scores):
    return max([s for s, cal in scores if cal == 500])


if __name__ == "__main__":
    ingredients = load_data(sys.argv[1])
    scores = get_scores(ingredients)
    print(f"Part 1: {part_1(scores)}")
    print(f"Part 2: {part_2(scores)}")
