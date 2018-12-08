import sys
from collections import defaultdict


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

    counts = defaultdict(lambda: 0)
    disqualified = set()

    for loc, dists in grid.items():
        mn = min(dists)
        if dists.count(mn) == 1:
            counts[dists.index(mn)] += 1
            if loc[0] in x or loc[1] in y:
                disqualified.add(dists.index(mn))

    most = 0
    for loc, count in counts.items():
        if loc not in disqualified and count > most:
            most = count

    return most


if __name__ == "__main__":
    print(answer(sys.argv[1]))
