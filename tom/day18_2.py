import sys
from collections import defaultdict, deque
from string import ascii_lowercase


def convert_to_int(fn):
    def wrapper(self, x, y):
        if str(y) in ascii_lowercase:
            y = self.r[y]
        fn(self, x, int(y))
    return wrapper


class Assembly:
    def __init__(self):
        self.i = 0
        self.count = 0
        self.d = deque()
        self.r = defaultdict(lambda: 0)
        self.waiting = False

    def snd(self, x):
        self.count += 1
        if x in ascii_lowercase:
            self.d.append(self.r[x])
        else:
            self.d.append(int(x))

    @convert_to_int
    def s(self, x, y):
        self.r[x] = y

    @convert_to_int
    def add(self, x, y):
        self.r[x] += y

    @convert_to_int
    def mul(self, x, y):
        self.r[x] *= y

    @convert_to_int
    def mod(self, x, y):
        self.r[x] %= y

    @convert_to_int
    def rcv(self, x, y):
        self.r[x] = y


def answer(file_path):
    with open(file_path, 'r') as f:
        commands = f.read().strip().split('\n')
    commands = dict(enumerate([cmd.split(' ') for cmd in commands]))
    a = [Assembly() for _ in range(2)]
    a[1].r['p'] = 1
    while True:
        for j in range(2):
            cmd = commands[a[j].i]
            if cmd[0] == 'jgz':
                first = cmd[1]
                if cmd[1] in ascii_lowercase:
                    first = a[j].r[first]
                first = int(first)
                if first > 0:
                    if str(cmd[2]) in ascii_lowercase:
                        a[j].i += a[j].r[cmd[2]]
                    else:
                        a[j].i += int(cmd[2])
                else:
                    a[j].i += 1
                continue
            elif cmd[0] == 'rcv':
                a[j].waiting = True
                if a[(j+1) % 2].d:
                    a[j].rcv(cmd[1], a[(j+1) % 2].d.popleft())
                    a[j].waiting = False
                else:
                    continue
            elif cmd[0] == 'snd':
                a[j].snd(cmd[1])
            elif cmd[0] == 'set':
                a[j].s(*cmd[1:])
            elif cmd[0] == 'add':
                a[j].add(*cmd[1:])
            elif cmd[0] == 'mul':
                a[j].mul(*cmd[1:])
            elif cmd[0] == 'mod':
                a[j].mod(*cmd[1:])
            a[j].i += 1
        if not all([0 <= a[j].i < len(commands) for j in range(2)]):
            break
        if all([a[j].waiting for j in range(2)]):
            break
    return a[1].count


if __name__ == "__main__":
    print(answer(sys.argv[1]))
