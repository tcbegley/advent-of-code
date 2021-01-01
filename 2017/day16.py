import sys


def load_data(path):
    with open(path) as f:
        return f.read().strip().split(",")


def spin(s, x):
    x = int(x)
    return s[-x:] + s[:-x]


def exchange(s, ab):
    pos = sorted(list(map(int, ab.split("/"))))
    return (
        s[: pos[0]]
        + s[pos[1]]
        + s[pos[0] + 1 : pos[1]]
        + s[pos[0]]
        + s[pos[1] + 1 :]
    )


def partner(s, ab):
    names = sorted(list(map(s.index, ab.split("/"))))
    return (
        s[: names[0]]
        + s[names[1]]
        + s[names[0] + 1 : names[1]]
        + s[names[0]]
        + s[names[1] + 1 :]
    )


def part_1(commands):
    s = "abcdefghijklmnop"
    moves = {"s": spin, "x": exchange, "p": partner}

    for cmd in commands:
        s = moves[cmd[0]](s, cmd[1:])

    return s


def part_2(commands):
    s, i = "abcdefghijklmnop", 0
    moves = {"s": spin, "x": exchange, "p": partner}

    while True:
        i += 1
        for cmd in commands:
            s = moves[cmd[0]](s, cmd[1:])
        if s == "abcdefghijklmnop":
            break

    for i in range(10 ** 9 % i):
        for cmd in commands:
            s = moves[cmd[0]](s, cmd[1:])

    return s


if __name__ == "__main__":
    commands = load_data(sys.argv[1])
    print(f"Part 1: {part_1(commands)}")
    print(f"Part 2: {part_2(commands)}")
