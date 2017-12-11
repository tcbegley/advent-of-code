import sys


def coordinate(steps):
    lookup = {'n': (0, 1), 's': (0, -1), 'ne': (1, 0), 'nw': (-1, 1),
              'se': (1, -1), 'sw': (-1, 0)}
    pos = [0, 0]
    for step in steps:
        pos[0] += lookup[step][0]
        pos[1] += lookup[step][1]
    return pos


def answer(file_path):
    with open(file_path, 'r') as f:
        steps = f.read().strip().split(',')
    locs = [coordinate(steps[:i]) for i in range(len(steps))]
    dists = []
    for loc in locs:
        if loc[0] * loc[1] > 0:
            dists.append(abs(loc[0]) + abs(loc[1]))
        else:
            dists.append(max(abs(loc[0]), abs(loc[1])))
    return max(dists)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
