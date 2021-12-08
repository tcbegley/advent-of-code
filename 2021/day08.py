import sys

LOCATIONS = "abcdefg"
VALID_DIGITS = {
    2: [{"c", "f"}],
    3: [{"a", "c", "f"}],
    4: [{"b", "c", "d", "f"}],
    5: [
        {"a", "c", "d", "e", "g"},
        {"a", "c", "d", "f", "g"},
        {"a", "b", "d", "f", "g"},
    ],
    6: [
        {"a", "b", "d", "e", "f", "g"},
        {"a", "b", "c", "e", "f", "g"},
        {"a", "b", "c", "d", "f", "g"},
    ],
    7: [{"a", "b", "c", "d", "e", "f", "g"}],
}
DIGIT_LOOKUP = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}


def load_data(path):
    def process_line(line):
        return [x.split(" ") for x in line.strip().split(" | ")]

    with open(path) as f:
        return [process_line(line) for line in f.readlines()]


def part_1(data):
    return sum(len(x) in {2, 3, 4, 7} for _, output in data for x in output)


def check_valid(mapping, numbers):
    for num in numbers:
        digits = {mapping[d] for d in num if d in mapping}
        if not any(digits <= valid for valid in VALID_DIGITS[len(num)]):
            return False
    return True


def map_segments(numbers):
    mapping = {}

    def backtrack(i=0):
        if i == 7:
            return mapping
        loc = LOCATIONS[i]
        available = set(LOCATIONS) - set(mapping.values())
        for candidate in available:
            mapping[loc] = candidate
            if check_valid(mapping, numbers):
                ret = backtrack(i + 1)
                if ret is not None:
                    return ret
            del mapping[loc]

    return backtrack()


def part_2(data):
    total = 0
    for numbers, outputs in data:
        mapping = map_segments(numbers)

        output = 0
        for o in outputs:
            output = (
                output * 10
                + DIGIT_LOOKUP["".join(sorted(mapping[d] for d in o))]
            )
        total += output

    return total


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
