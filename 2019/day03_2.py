import sys


def get_locs(move, base):
    x, y, n = base
    d, steps = move[0], int(move[1:])

    if d in ("R", "L"):
        delta = 1 if d == "R" else -1
        return (
            [((x + (i + 1) * delta, y), n + i + 1) for i in range(steps)],
            (x + steps * delta, y, n + steps),
        )

    delta = 1 if d == "U" else -1
    return (
        [((x, y + (i + 1) * delta), n + i + 1) for i in range(steps)],
        (x, y + steps * delta, n + steps),
    )


def answer(path):
    with open(path) as f:
        wire1, wire2 = f.read().strip().split("\n")
        wire1 = wire1.strip().split(",")
        wire2 = wire2.strip().split(",")

    loc = (0, 0, 0)
    locs1 = {}
    for move in wire1:
        locs, loc = get_locs(move, loc)
        tmp = dict(locs)
        tmp.update(locs1)
        locs1 = tmp

    loc = (0, 0, 0)
    locs2 = {}
    for move in wire2:
        locs, loc = get_locs(move, loc)
        tmp = dict(locs)
        tmp.update(locs2)
        locs2 = tmp

    intersection = set(locs1) & set(locs2)

    return min([locs1[l] + locs2[l] for l in intersection])


if __name__ == "__main__":
    print(answer(sys.argv[1]))
