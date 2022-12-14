import sys


def power_level(x, y, serial_no):
    rack_id = x + 10
    power = rack_id * (rack_id * y + serial_no)
    return (power // 100) % 10 - 5


def load_data(path):
    with open(path) as f:
        serial_no = int(f.read().strip())

    # add an extra row and column of zeros to make indexing easier
    prefix_sums = [[0] * 301 for _ in range(301)]
    for x in range(1, 301):
        for y in range(1, 301):
            prefix_sums[x][y] = (
                power_level(x, y, serial_no)
                + prefix_sums[x - 1][y]
                + prefix_sums[x][y - 1]
                - prefix_sums[x - 1][y - 1]
            )

    return prefix_sums


def search(prefix_sums, s):
    best = float("-inf")
    best_x, best_y = None, None

    for y in range(1, 302 - s):
        for x in range(1, 302 - s):
            total = (
                prefix_sums[x + s - 1][y + s - 1]
                - prefix_sums[x + s - 1][y - 1]
                - prefix_sums[x - 1][y + s - 1]
                + prefix_sums[x - 1][y - 1]
            )
            if total > best:
                best, best_x, best_y = total, x, y

    return best, best_x, best_y


def part_1(prefix_sums):
    _, x, y = search(prefix_sums, s=3)
    return x, y


def part_2(prefix_sums):
    best = float("-inf")
    best_x, best_y, best_s = None, None, None

    for s in range(1, 301):
        if best_s is not None and s > best_s + 5:
            # if we've not improved for the last 5 steps of s, end search
            break
        s_best, s_best_x, s_best_y = search(prefix_sums, s)
        if s_best > best:
            best, best_x, best_y, best_s = s_best, s_best_x, s_best_y, s

    return best_x, best_y, best_s


if __name__ == "__main__":
    prefix_sums = load_data(sys.argv[1])
    print(f"Part 1: {part_1(prefix_sums)}")
    print(f"Part 2: {part_2(prefix_sums)}")
