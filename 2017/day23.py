import sys
from collections import defaultdict
from string import ascii_lowercase


def load_data(path):
    with open(path) as f:
        return f.read().strip().split("\n")


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


def part_1(commands):
    commands = dict(enumerate([command.split(" ") for command in commands]))
    c = Coprocessor()
    while 0 <= c.i < len(commands):
        cmd = commands[c.i]
        if cmd[0] == "jnz":
            c.jnz(*cmd[1:])
            continue
        elif cmd[0] == "set":
            c.s(*cmd[1:])
        elif cmd[0] == "sub":
            c.sub(*cmd[1:])
        elif cmd[0] == "mul":
            c.mul(*cmd[1:])
        c.i += 1
    return c.mul_count


def part_2():
    # hard coded version of my input...
    b = 57
    c = b
    b *= 100
    b += 100000
    c = b
    c += 17000
    h = 0
    for b in range(105700, 122701, 17):
        f = 1
        d = 2
        for d in range(2, b):
            if b % d == 0:
                f = 0
                break
        if f == 0:
            h += 1

    return h


if __name__ == "__main__":
    commands = load_data(sys.argv[1])
    print(f"Part 1: {part_1(commands)}")
    print(f"Part 2: {part_2()}")
