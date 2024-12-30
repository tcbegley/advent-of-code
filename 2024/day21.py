import sys
from functools import cache

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


def complexity(code, n_robots=2):
    @cache
    def min_seq_length(seq, robots):
        if robots == 0:
            return len(seq)

        total = 0
        for start, end in zip("A" + seq, seq):
            diff_r = int((ARROW_KEYPAD_LOCS[end] - ARROW_KEYPAD_LOCS[start]).real)
            diff_i = int((ARROW_KEYPAD_LOCS[end] - ARROW_KEYPAD_LOCS[start]).imag)
            if end == "<" and start in "^A":
                seqs = ["v" + "<" * abs(diff_r) + "A"]
            elif end in "^A" and start == "<":
                seqs = [">" * abs(diff_r) + "^" + "A"]
            else:
                v_char = "v" if diff_i < 0 else "^"
                h_char = "<" if diff_r < 0 else ">"
                seqs = list(
                    {
                        v_char * abs(diff_i) + h_char * abs(diff_r) + "A",
                        h_char * abs(diff_r) + v_char * abs(diff_i) + "A",
                    }
                )
            total += min(min_seq_length(seq, robots - 1) for seq in seqs)

        return total

    length = 0
    for start, end in zip("A" + code, code):
        diff_r = int((NUMERIC_KEYPAD_LOCS[end] - NUMERIC_KEYPAD_LOCS[start]).real)
        diff_i = int((NUMERIC_KEYPAD_LOCS[end] - NUMERIC_KEYPAD_LOCS[start]).imag)
        if end in "741" and start in "0A":
            seqs = ["^" * abs(diff_i) + "<" * abs(diff_r) + "A"]
        elif end in "0A" and start in "741":
            seqs = [">" * abs(diff_r) + "v" * abs(diff_i) + "A"]
        else:
            v_char = "v" if diff_i < 0 else "^"
            h_char = "<" if diff_r < 0 else ">"
            seqs = list(
                {
                    v_char * abs(diff_i) + h_char * abs(diff_r) + "A",
                    h_char * abs(diff_r) + v_char * abs(diff_i) + "A",
                }
            )
        length += min(min_seq_length(seq, n_robots) for seq in seqs)

    return length * int(code[:-1])


def part_1(data):
    return sum(complexity(code) for code in data)


def part_2(data):
    return sum(complexity(code, n_robots=25) for code in data)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
