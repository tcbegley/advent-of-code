import sys


def load_data(path):
    def process_line(line):
        _, arg = line.rsplit(" ", 1)
        return int(arg)

    with open(path) as f:
        lines = f.readlines()

    # all blocks are basically the same except for integer literals on 3 lines
    return [
        (
            process_line(lines[i + 4]),
            process_line(lines[i + 5]),
            process_line(lines[i + 15]),
        )
        for i in range(0, len(lines), 18)
    ]


def check_assumptions(args):
    # each block takes three arguments, a, b, c. There is some structure to the
    # input that helps us find a solution that we should check for new inputs

    # a is always either 1 or 26
    assert all(a == 1 or a == 26 for a, *_ in args)

    # a == 1 occurs as often as a == 26
    assert len([a for a, *_ in args if a == 1]) == len([a for a, *_ in args if a == 26])

    # when a == 1, b >= 10
    # when a == 26, b < 0
    assert all((a == 1 and b >= 10) or (a == 26 and b < 0) for a, b, _ in args)

    # c + d for d = 1,...,9 is always between 0 and 25 inclusive
    assert all(0 <= c + 1 and c + 9 < 26 for _, _, c in args)


# this is not actually required for finding the solution, but is helpful for
# verifying that our solution is a valid one
def process_block(w, z, args):
    # given an input w, current value of z and the three integer literals,
    # calculate z after processing this block
    a, b, c = args

    if ((z % 26) + b) != w:
        return (z // a) * 26 + (w + c)
    return z // a


# Notice that since we have checked that b >= 10 whenever a == 1, we know that
# ((z % 26) + b) != w will always be satisfied for any w = 1,...,9 when a == 1
# hence when a == 1 we have:  z = z * 21 + (w + c)

# moreover we know that w + c is in the range 0, ..., 26 for all w, so this
# is like appending a digit to a number in base 26 (multiply the existing
# number by 26, then append another non-negative number less than 26)

# hence we can only ever return z // a if a == 26. for this to be zero on the
# last step, z must have been less than 26. Hence on the previous step it must
# have been less than 26^2 etc. thinking again about numbers in base 26, this
# division is equivalent to removing the least significant digit

# since we have checked that there are the same number of a == 1 as a == 26,
# and we know that a == 1 is equivalent to adding a digit to our base 26 number
# we need to make sure that every time we see a == 26 we pop off a digit. that
# means we need to ensure that (z % 26) + b == w

# z % 26 is equal to the last digit of the base 26 number, i.e. w + c for the
# most recent occurence of a == 1. hence we need to satisfy:

# w = w_old + c_old + b

# together with the constraint that w and w_old are one of 1,...,9, we can
# choose each pair to be maximal (or minimal) to ensure equality, which will
# give us the answer


def get_valid_input(args, minimise=False):
    stack = []
    model_input = [0] * 14
    for i, (a, b, c) in enumerate(args):
        if a == 1:
            # a == 1 corresponds to a digit being appended
            stack.append((i, c))
        else:
            i_old, c_old = stack.pop()
            # we need to satisfy
            # model_input[i] = model_input[i_old] + c_old + b
            if (diff := c_old + b) >= 0:
                if minimise:
                    # model_input[i_old] must be at least 1
                    model_input[i] = 1 + diff
                    model_input[i_old] = 1
                else:
                    # model_input[i] is at most 9
                    model_input[i] = 9
                    model_input[i_old] = 9 - diff
            else:
                if minimise:
                    # model_input[i] is at least 1
                    model_input[i] = 1
                    model_input[i_old] = 1 - diff
                else:
                    # model_input[i_old] is at most 9
                    model_input[i] = 9 + diff
                    model_input[i_old] = 9

    # check that our solution does actually work
    assert (1 <= w <= 9 for w in model_input)

    z = 0
    for arg, w in zip(args, model_input):
        z = process_block(w, z, arg)
    assert z == 0

    return "".join(map(str, model_input))


def part_1(args):
    return get_valid_input(args)


def part_2(args):
    return get_valid_input(args, minimise=True)


if __name__ == "__main__":
    args = load_data(sys.argv[1])
    check_assumptions(args)
    print(f"Part 1: {part_1(args)}")
    print(f"Part 2: {part_2(args)}")
