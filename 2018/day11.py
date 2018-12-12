import sys


def get_power_level(x, y, s):
    rid = x + 10
    pl = rid * y
    pl += s
    pl *= rid
    pl = (pl % 1000) // 100
    return pl - 5


def answer(serial_no):
    grid = [[None] * 300 for _ in range(300)]

    for i in range(300):
        for j in range(300):
            grid[i][j] = get_power_level(i, j, serial_no)

    best = -float("inf")
    bestx = None
    besty = None

    for x in range(298):
        for y in range(298):
            total = sum(
                [
                    grid[x + i][y + j]
                    for i in range(3)
                    for j in range(3)
                ]
            )
            if total > best:
                best = total
                bestx = x
                besty = y

    return bestx, besty


if __name__ == "__main__":
    print(answer(int(sys.argv[1])))
