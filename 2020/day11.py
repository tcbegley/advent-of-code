import sys
from itertools import product


def load_data(path):
    with open(path) as f:
        return [list(row) for row in f.read().strip().split("\n")]


def get_neighbours_1(seats, i, j):
    for r in range(i - 1, i + 2):
        for c in range(j - 1, j + 2):
            if r == i and c == j:
                continue
            if 0 <= r < len(seats) and 0 <= c < len(seats[0]):
                yield seats[r][c]


def get_neighbours_2(seats, i, j):
    dirs = [d for d in product((-1, 0, 1), (-1, 0, 1)) if d != (0, 0)]

    rows = len(seats)
    cols = len(seats[0])

    for x, y in dirs:
        alpha = 1
        while 0 <= (r := i + alpha * x) < rows and 0 <= (c := j + alpha * y) < cols:
            if seats[r][c] != ".":
                yield seats[r][c]
                break
            else:
                alpha += 1


def simulate_step(seats, tol, get_neighbours):
    new_seats = [row[:] for row in seats]

    rows = len(new_seats)
    cols = len(new_seats[0])

    for i in range(rows):
        for j in range(cols):
            nbrs = get_neighbours(seats, i, j)

            if seats[i][j] == "L" and sum(seat == "#" for seat in nbrs) == 0:
                new_seats[i][j] = "#"
            elif seats[i][j] == "#" and sum(seat == "#" for seat in nbrs) >= tol:
                new_seats[i][j] = "L"

    return new_seats


def to_string(seats):
    # new lines not strictly necessary but useful for debugging
    return "\n".join(["".join(row) for row in seats])


def simulate(seats, tol, get_neighbours):
    seen = {to_string(seats)}

    while True:
        seats = simulate_step(seats, tol=tol, get_neighbours=get_neighbours)
        s = to_string(seats)

        if s in seen:
            break

        seen.add(s)

    return s.count("#")


def part_1(seats):
    return simulate(seats, tol=4, get_neighbours=get_neighbours_1)


def part_2(seats):
    return simulate(seats, tol=5, get_neighbours=get_neighbours_2)


if __name__ == "__main__":
    seats = load_data(sys.argv[1])
    print(f"Part 1: {part_1(seats)}")
    print(f"Part 2: {part_2(seats)}")
