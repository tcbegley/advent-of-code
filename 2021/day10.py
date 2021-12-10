import sys

CORRUPTED_POINTS = {")": 3, "]": 57, "}": 1197, ">": 25137}
AUTOCOMPLETE_POINTS = {")": 1, "]": 2, "}": 3, ">": 4}
MATCH = {")": "(", "]": "[", "}": "{", ">": "<"}
INV_MATCH = {v: k for k, v in MATCH.items()}


def load_data(path):
    with open(path) as f:
        return [line.strip() for line in f.readlines()]


def score_corrupted(line):
    stack = []
    for char in line:
        if char in MATCH:
            if not stack or stack[-1] != MATCH[char]:
                return CORRUPTED_POINTS[char]
            stack.pop()
        else:
            stack.append(char)

    return 0


def autocomplete_score(line):
    stack = []
    for char in line:
        if char in MATCH:
            if not stack or stack[-1] != MATCH[char]:
                raise ValueError("This shouldn't be called on corrupted lines")
            stack.pop()
        else:
            stack.append(char)

    remaining = "".join(INV_MATCH[char] for char in reversed(stack))

    score = 0
    for char in remaining:
        score = score * 5 + AUTOCOMPLETE_POINTS[char]

    return score


def part_1(data):
    return sum(score_corrupted(line) for line in data)


def part_2(data):
    # filter corrupted lines
    data = [line for line in data if score_corrupted(line) == 0]
    # get scores
    scores = sorted([autocomplete_score(line) for line in data])
    return scores[len(scores) // 2]


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
