import sys
from collections import defaultdict
from string import ascii_lowercase


class Assembly:
    def __init__(self):
        self.r = defaultdict(lambda: 0)
        self.r['last'] = None

    def snd(self, x):
        self.r['last'] = self.r[x]

    def s(self, x, y):
        if y in ascii_lowercase:
            self.r[x] = self.r[y]
        else:
            self.r[x] = int(y)

    def add(self, x, y):
        if y in ascii_lowercase:
            self.r[x] += self.r[y]
        else:
            self.r[x] += int(y)

    def mul(self, x, y):
        if y in ascii_lowercase:
            self.r[x] *= self.r[y]
        else:
            self.r[x] *= int(y)

    def mod(self, x, y):
        if y in ascii_lowercase:
            self.r[x] %= self.r[y]
        else:
            self.r[x] %= int(y)

    def rcv(self):
        return self.r['last']


def answer(file_path):
    with open(file_path, 'r') as f:
        commands = f.read().strip().split('\n')
    commands = dict(enumerate([cmd.split(' ') for cmd in commands]))
    a = Assembly()
    i = 0
    while i >= 0 and i < len(commands):
        cmd = commands[i]
        if cmd[0] == 'jgz' and a.r[cmd[1]] > 0:
            if str(cmd[2]) in ascii_lowercase:
                i += a.r[cmd[2]]
            else:
                i += int(cmd[2])
            continue
        i += 1
        if cmd[0] == 'snd':
            a.snd(cmd[1])
        if cmd[0] == 'set':
            a.s(*cmd[1:])
        if cmd[0] == 'add':
            a.add(*cmd[1:])
        if cmd[0] == 'mul':
            a.mul(*cmd[1:])
        if cmd[0] == 'mod':
            a.mod(*cmd[1:])
        if cmd[0] == 'rcv':
            rcv = a.rcv()
            if rcv:
                return rcv


if __name__ == "__main__":
    print(answer(sys.argv[1]))
