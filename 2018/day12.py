import sys


def load_data(path):
    with open(path) as f:
        init_state, rules = f.read().strip().split("\n\n")
    init_state = init_state.removeprefix("initial state: ")
    rules = dict(row.split(" => ") for row in rules.split("\n"))
    return init_state, rules


def score(state, left):
    return sum(i for i, p in enumerate(state, start=left) if p == "#")


def solve(init_state, rules, n=20):
    # my input seems to settle down to a fixed state that moves right one
    # space each time, but this code should work for any repeating cycle
    state, left = init_state, 0
    seen = {}
    states = []

    for i in range(n):
        left += state.index("#")
        state = state.strip(".")

        if state in seen:
            prev_left, prev_i = seen[state]
            # cycle_length is number of steps taken since we last saw the
            # repeated state
            cycle_length = i - prev_i
            # how many cycles + remainder to reach our target
            n_cycles, offset = divmod(n - i, cycle_length)
            # increment the left cursor by the number of cycles times the
            # amount the cursor moved during the last cycle, plus the offset
            left += n_cycles * (left - prev_left) + (
                states[prev_i + offset][1] - states[prev_i][1]
            )
            return score(states[prev_i + offset][0], left)

        seen[state] = (left, i)
        states.append((state, left))

        left -= 4
        state = f"....{state}...."

        left += 2
        state = "".join(
            rules.get(state[i - 2 : i + 3], ".") for i in range(2, len(state) - 2)
        )

    return score(state, left)


def part_1(init_state, rules):
    return solve(init_state, rules)


def part_2(init_state, rules):
    return solve(init_state, rules, 50_000_000_000)


if __name__ == "__main__":
    init_state, rules = load_data(sys.argv[1])
    print(f"Part 1: {part_1(init_state, rules)}")
    print(f"Part 2: {part_2(init_state, rules)}")
