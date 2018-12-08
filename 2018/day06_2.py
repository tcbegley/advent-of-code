import sys


def answer(path):
    with open(path) as f:
        coords = [
            [int(i) for i in c.split(",")]
            for c in f.read().strip().split(("\n"))
        ]
    x = (
        min(coords, key=lambda c: c[0])[0],
        max(coords, key=lambda c: c[0])[0],
    )
    y = (
        min(coords, key=lambda c: c[1])[1],
        max(coords, key=lambda c: c[1])[1],
    )

    grid = {}

    for i in range(x[0], x[1] + 1):
        for j in range(y[0], y[1] + 1):
            grid[(i, j)] = [abs(i - c[0]) + abs(j - c[1]) for c in coords]

    locs = 0

    for loc, dists in grid.items():
        if sum(dists) < 10000:
            locs += 1

    return locs


if __name__ == "__main__":
    print(answer(sys.argv[1]))
