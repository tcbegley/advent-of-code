import sys


def load_data(path):
    with open(path) as f:
        return [x.strip().split(" ") for x in f.readlines()]


def no_anagrams(pass_phrases):
    pass_phrases = [sorted(list(pp)) for pp in pass_phrases]
    return not any(pass_phrases.count(pp) > 1 for pp in pass_phrases)


def part_1(pass_phrases):
    return len([pp for pp in pass_phrases if len(pp) == len(set(pp))])


def part_2(pass_phrases):
    return len([pp for pp in pass_phrases if no_anagrams(pp)])


if __name__ == "__main__":
    pass_phrases = load_data(sys.argv[1])
    print(f"Part 1: {part_1(pass_phrases)}")
    print(f"Part 2: {part_2(pass_phrases)}")
