import sys
from collections import deque
from itertools import product


def process_row(row):
    lights, *buttons, joltage = row.split(" ")
    lights = tuple(c == "#" for c in lights.strip("[]"))
    buttons = [tuple(map(int, button.strip("()").split(","))) for button in buttons]
    joltage = tuple(map(int, joltage.strip(r"{}").split(",")))
    return lights, buttons, joltage


def load_data(path):
    with open(path) as f:
        return [process_row(row) for row in f.read().strip().split("\n")]


def bfs(lights, buttons):
    state = tuple(False for _ in lights)
    seen = {state}
    queue = deque([(0, state)])

    while queue:
        presses, state = queue.popleft()

        if state == lights:
            return presses

        for button in buttons:
            new_state = tuple(
                not light if i in button else light for i, light in enumerate(state)
            )
            if new_state not in seen:
                queue.append((presses + 1, new_state))
                seen.add(new_state)


def part_1(data):
    return sum(bfs(lights, buttons) for lights, buttons, _ in data)


def reduce_rows(A, b, row, col, pivot):
    # swap the row with the non-zero entry to the top
    A[pivot], A[row] = A[row], A[pivot]
    b[pivot], b[row] = b[row], b[pivot]

    # ensure leading value in row is 1
    norm = 1 / A[row][col]
    b[row] *= norm
    for c in range(col, len(A[0])):
        A[row][c] *= norm

    # now zero out the remaining rows
    for r in range(row + 1, len(A)):
        if A[r][col] != 0:
            m = -A[r][col] / A[row][col]
            for c in range(col, len(A[0])):
                A[r][c] += m * A[row][c]
            b[r] += m * b[row]


def invert(A, b, free_indices, vals):
    # because A is in RREF, we can reconstruct the solution easily
    # first create an empty solution vector, and populate the free indices with the
    # chosen values
    x = [0] * len(A[0])
    for idx, val in zip(free_indices, vals):
        x[idx] = val

    # next, iterating over rows in reverse order, we can fill in the entry of x that has
    # the same index as the first non-zero entry of the row (which is not only non-zero,
    # but is in fact 1). A simple linear inversion of sum_i A[r][i] * x[i] = b[r] is
    # x[idx] = b[r] - sum_idx^len(row) A[r][i] * x[i]
    for r in range(len(A) - 1, -1, -1):
        row = A[r]
        try:
            idx = row.index(1)
        except ValueError:
            continue

        rhs = [row[i] * x[i] for i in range(idx + 1, len(x))]
        x[idx] = b[r] - sum(rhs)

    return x


def min_presses(buttons, joltage):
    n_buttons = len(buttons)
    n_lights = len(joltage)

    A = [[0] * n_buttons for _ in range(n_lights)]
    for r in range(n_lights):
        for c, button in enumerate(buttons):
            if r in button:
                A[r][c] = 1
    b = list(joltage)
    # we want to find x such that A @ x = b. obviously we would ideally import
    # some linear programming library here, but the rules i've set myself are standard
    # library only... so here we go!

    # A will not have full rank in general, so we need to compute reduced row echelon
    # form... we will keep track of which variables end up "free", and which can be
    # determined from the free variables. In RREF the free variables are the ones that
    # do not have a leading 1 in one of the rows
    free_variables = [True] * n_buttons
    row = 0
    for col in range(n_buttons):
        for pivot in range(row, n_lights):
            # find a row with a non-zero entry in col
            if A[pivot][col] != 0:
                reduce_rows(A, b, row, col, pivot)
                free_variables[col] = False
                row += 1
                break

    # construct the search space, i.e. find the possible values of each free variable
    # by figuring out which lights the buttons increment and using that to upper bound
    # the number of presses. then use itertools.product to make a grid search
    grid = []
    free_indices = []
    for i, free in enumerate(free_variables):
        if free:
            grid.append(range(min([joltage[b] for b in buttons[i]]) + 1))
            free_indices.append(i)

    # do the actual grid search, for each combination of free variables, we can invert
    # the matrix
    solutions = []
    for vals in product(*grid):
        solution = invert(A, b, free_indices, vals)
        if all(round(i) >= 0 and abs(round(i) - i) <= 1e-6 for i in solution):
            # non-free variables must be non-negative and integer
            solutions.append(solution)
    return round(min(sum(solution) for solution in solutions))


def part_2(data):
    return sum(min_presses(buttons, joltage) for _, buttons, joltage in data)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
