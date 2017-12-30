import sys
from string import ascii_uppercase as auc


class Explorer:
    dirs = {'n': [-1, 0], 's': [1, 0], 'e': [0, 1], 'w': [0, -1]}

    def __init__(self, m):
        self.m = m
        self.x = 0
        self.y = self.find_y_start()
        self.cur_dir = 's'
        self.seen = []
        self.count = 0

    def find_y_start(self):
        for i in range(len(self.m[0])):
            if self.m[0][i] != ' ':
                return i

    def choose_next_dir(self):
        if self.cur_dir in ['n', 's']:
            if self.y > 0 and self.m[self.x][self.y-1] in auc + '-':
                self.cur_dir = 'w'
            else:
                self.cur_dir = 'e'
        else:
            if self.x > 0 and self.m[self.x-1][self.y] in auc + '|':
                self.cur_dir = 'n'
            else:
                self.cur_dir = 's'

    def explore(self):
        while True:
            self.count += 1
            cur_loc = self.m[self.x][self.y]
            if cur_loc == ' ':
                break
            if cur_loc == '+':
                self.choose_next_dir()
            if cur_loc in auc:
                self.seen.append(cur_loc)
            self.x, self.y = [
                l + d for l, d in zip(
                    (self.x, self.y), Explorer.dirs[self.cur_dir]
                )
            ]


def answer(file_path):
    with open(file_path, 'r') as f:
        m = [[c for c in row] for row in f.read().split('\n')]
    e = Explorer(m)
    e.explore()
    return e.count - 1


if __name__ == "__main__":
    print(answer(sys.argv[1]))
