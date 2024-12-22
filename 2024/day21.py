import sys

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+

NUMERIC_KEYPAD_LOCS = {
    "7": 3j,
    "8": 1 + 3j,
    "9": 2 + 3j,
    "4": 2j,
    "5": 1 + 2j,
    "6": 2 + 2j,
    "1": 1j,
    "2": 1 + 1j,
    "3": 2 + 1j,
    "0": 1,
    "A": 2,
}
ARROW_KEYPAD_LOCS = {"^": 1 + 1j, "A": 2 + 1j, "<": 0, "v": 1, ">": 2}


def load_data(path):
    with open(path) as f:
        return f.read().strip().split("\n")


def make_numeric_lookup():
    lookup = {}
    for start, start_loc in NUMERIC_KEYPAD_LOCS.items():
        d = lookup.setdefault(start, {})
        for end, end_loc in NUMERIC_KEYPAD_LOCS.items():
            diff_r = int((end_loc - start_loc).real)
            diff_i = int((end_loc - start_loc).imag)
            horiz = ">" if diff_r > 0 else "<"
            vert = "^" if diff_i > 0 else "v"
            if start in "0A" and end in "147":
                d[end] = vert * abs(diff_i) + horiz * abs(diff_r)
            else:
                d[end] = horiz * abs(diff_r) + vert * abs(diff_i)

    return lookup


def make_directional_lookup():
    lookup = {}
    for start, start_loc in ARROW_KEYPAD_LOCS.items():
        d = lookup.setdefault(start, {})
        for end, end_loc in ARROW_KEYPAD_LOCS.items():
            diff_r = int((end_loc - start_loc).real)
            diff_i = int((end_loc - start_loc).imag)
            horiz = ">" if diff_r > 0 else "<"
            if diff_i > 0:
                d[end] = horiz * abs(diff_r) + "^" * abs(diff_i)
            else:
                d[end] = "v" * abs(diff_i) + horiz * abs(diff_r)

    return lookup


def number_to_directions(code, numeric_lookup):
    out = ""
    loc = "A"
    for c in code:
        out += numeric_lookup[loc][c] + "A"
        loc = c
    return out


def directions_to_directions(directions, directional_lookup):
    out = ""
    d = "A"
    for c in directions:
        out += directional_lookup[d][c] + "A"
        d = c
    return out


def complexity(code, numeric_lookup, directional_lookup):
    keys = number_to_directions(code, numeric_lookup)
    for _ in range(2):
        keys = directions_to_directions(keys, directional_lookup)

    return len(keys) * int(code.removesuffix("A"))


def part_1(data):
    numeric_lookup = make_numeric_lookup()
    directional_lookup = make_directional_lookup()

    return sum(complexity(code, numeric_lookup, directional_lookup) for code in data)


def part_2(data):
    pass


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")


"""
<A>A: <vA <A A >>^A A vA <^A >A A vA ^A <vA >^A A <A >A <v<A >A >^A
<A>A: v<<A >>^A A v<A <A >>^A A vA A <^A >A v<A >^A A <A >A v<A <A >>^A


^A <<^^A >>A vvvA

379A


<A >A v<<A A >^A A >A vA A ^A v<A A A >^A

<A >A v<<A A >^A A >A vA A ^A <vA A A >^A
<A >A <A A v<A A >>^A vA A ^A v<A A A >^A

^A ^^<<A >>A vvvA

379A


v<<A >>^A A v<A <A >>^A A vA A <^A >A
<A A v<A A >>^A

^^<<A

v<A <A A >>^A A vA <^A >A A vA ^A
v<<A A >^A A >A

<<^^A

# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+

#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
"""
