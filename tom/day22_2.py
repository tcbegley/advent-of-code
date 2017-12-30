import sys
from collections import defaultdict


class Carrier:
    dirs = {'n': (-1, 0), 's': (1, 0), 'e': (0, 1), 'w': (0, -1)}
    new_dir = {
        '.': dict(zip('nesw', 'wnes')),
        'W': dict(zip('nesw', 'nesw')),
        '#': dict(zip('nesw', 'eswn')),
        'F': dict(zip('nesw', 'swne'))
    }
    update = dict(zip('.W#F', 'W#F.'))

    def __init__(self, m):
        self.cur_dir = 'n'
        self.x = 0
        self.y = 0
        self.world = defaultdict(lambda: '.')
        self.initialise_world(m)
        self.infected = 0

    def initialise_world(self, m):
        r = len(m)
        c = len(m[0])
        for i in range(r):
            for j in range(c):
                self.world[(i-r//2, j-c//2)] = m[i][j]

    def move(self):
        cur_loc = self.world[(self.x, self.y)]
        self.cur_dir = Carrier.new_dir[cur_loc][self.cur_dir]
        self.world[(self.x, self.y)] = Carrier.update[cur_loc]
        if cur_loc == 'W':
            self.infected += 1
        self.x, self.y = [
            l + d for l, d in zip(
                (self.x, self.y), Carrier.dirs[self.cur_dir]
            )
        ]


def answer(file_path):
    with open(file_path, 'r') as f:
        m = f.read().strip().split('\n')
    c = Carrier(m)
    for _ in range(10000000):
        c.move()
    return c.infected


if __name__ == "__main__":
    print(answer(sys.argv[1]))
