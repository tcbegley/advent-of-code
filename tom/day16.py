import sys


def spin(s, x):
    x = int(x)
    return s[-x:] + s[:-x]


def exchange(s, ab):
    pos = sorted(list(map(int, ab.split('/'))))
    return (s[:pos[0]] + s[pos[1]] + s[pos[0]+1:pos[1]] +
            s[pos[0]] + s[pos[1]+1:])


def partner(s, ab):
    names = sorted(list(map(s.index, ab.split('/'))))
    return (s[:names[0]] + s[names[1]] + s[names[0]+1:names[1]] +
            s[names[0]] + s[names[1]+1:])


def answer(file_path):
    with open(file_path, 'r') as f:
        commands = f.read().strip().split(',')
    s = 'abcdefghijklmnop'
    moves = {'s': spin, 'x': exchange, 'p': partner}
    for cmd in commands:
        s = moves[cmd[0]](s, cmd[1:])
    return s


if __name__ == "__main__":
    print(answer(sys.argv[1]))
