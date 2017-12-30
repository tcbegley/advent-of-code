import sys
from collections import defaultdict
from string import ascii_lowercase


def convert_to_int(fn):
    def wrapper(self, x, y):
        if str(y) in ascii_lowercase:
            y = self.r[y]
        fn(self, x, int(y))
    return wrapper


class Coprocessor:
    def __init__(self):
        self.i = 0
        self.r = defaultdict(lambda: 0)
        self.mul_count = 0

    @convert_to_int
    def s(self, x, y):
        self.r[x] = y

    @convert_to_int
    def mul(self, x, y):
        self.mul_count += 1
        self.r[x] *= y

    @convert_to_int
    def sub(self, x, y):
        self.r[x] -= y

    @convert_to_int
    def jnz(self, x, y):
        if x in ascii_lowercase:
            x = int(self.r[x])
        else:
            x = int(x)
        if x != 0:
            self.i += y
        else:
            self.i += 1


def answer(file_path):
    with open(file_path, 'r') as f:
        commands = f.read().strip().split('\n')
    commands = dict(enumerate([command.split(' ') for command in commands]))
    c = Coprocessor()
    while 0 <= c.i < len(commands):
        cmd = commands[c.i]
        if cmd[0] == 'jnz':
            c.jnz(*cmd[1:])
            continue
        elif cmd[0] == 'set':
            c.s(*cmd[1:])
        elif cmd[0] == 'sub':
            c.sub(*cmd[1:])
        elif cmd[0] == 'mul':
            c.mul(*cmd[1:])
        c.i += 1
    return c.mul_count


if __name__ == "__main__":
    print(answer(sys.argv[1]))
