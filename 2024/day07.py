import re
import sys

NUMBER_PATTERN = re.compile(r"\d+")


def load_data(path):
    with open(path) as f:
        return [
            [int(n) for n in NUMBER_PATTERN.findall(row)]
            for row in f.read().strip().split("\n")
        ]


def check(answer, total, args):
    if not args:
        return answer == total
    return answer > total and (
        check(answer, total + args[0], args[1:])
        or check(answer, total * args[0], args[1:])
    )


def check2(answer, total, args):
    if not args:
        return answer == total
    return answer > total and (
        check2(answer, total + args[0], args[1:])
        or check2(answer, total * args[0], args[1:])
        or check2(answer, int(str(total) + str(args[0])), args[1:])
    )


def part_1(data):
    return sum(answer for answer, total, *args in data if check(answer, total, args))


def part_2(data):
    return sum(answer for answer, total, *args in data if check2(answer, total, args))


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
