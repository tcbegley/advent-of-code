import sys


def load_data(path):
    with open(path) as f:
        return f.read().strip().split("\n")


def part_1(directions):
    keypad = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
    code = ""
    loc = (1, 1)
    for direction in directions:
        for c in direction:
            if c == "U":
                loc = (max(loc[0] - 1, 0), loc[1])
            elif c == "R":
                loc = (loc[0], min(loc[1] + 1, 2))
            elif c == "D":
                loc = (min(loc[0] + 1, 2), loc[1])
            elif c == "L":
                loc = (loc[0], max(loc[1] - 1, 0))
        code += keypad[loc[0]][loc[1]]
    return code


def part_2(directions):
    keypad = [
        [None, None, "1", None, None],
        [None, "2", "3", "4", None],
        ["5", "6", "7", "8", "9"],
        [None, "A", "B", "C", None],
        [None, None, "D", None, None],
    ]

    code = ""
    loc = (2, 0)
    for direction in directions:
        for c in direction:
            if c == "U":
                loc = (max(loc[0] - 1, 2 - loc[1], loc[1] - 2), loc[1])
            elif c == "R":
                loc = (loc[0], min(loc[1] + 1, 6 - loc[0], loc[0] + 2))
            elif c == "D":
                loc = (min(loc[0] + 1, 6 - loc[1], loc[1] + 2), loc[1])
            elif c == "L":
                loc = (loc[0], max(loc[1] - 1, 2 - loc[0], loc[0] - 2))
        code += keypad[loc[0]][loc[1]]
    return code


if __name__ == "__main__":
    directions = load_data(sys.argv[1])
    print(f"Part 1: {part_1(directions)}")
    print(f"Part 2: {part_2(directions)}")
