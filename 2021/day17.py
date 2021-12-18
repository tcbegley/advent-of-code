import re
import sys

INTEGER_PATTERN = re.compile(r"\-?[0-9]+")


def load_data(path):
    with open(path) as f:
        x_min, x_max, y_min, y_max = [
            int(i) for i in INTEGER_PATTERN.findall(f.read())
        ]
    if max(x_min, x_max) < 0:
        # wlog can assume target is in positive x direction
        return -x_max, -x_min, y_min, y_max
    return x_min, x_max, y_min, y_max


def part_1(y_min):
    return -y_min * (-y_min - 1) // 2


def part_2(x_min, x_max, y_min, y_max):
    total = 0
    for vx_0 in range(1, x_max + 1):
        for vy_0 in range(y_min, -y_min):
            x, y = 0, 0
            vx, vy = vx_0, vy_0

            while x <= x_max and y >= y_min:
                if x >= x_min and y <= y_max:
                    total += 1
                    break
                x += vx
                vx = max(0, vx - 1)
                y += vy
                vy -= 1
    return total


if __name__ == "__main__":
    x_min, x_max, y_min, y_max = load_data(sys.argv[1])
    print(f"Part 1: {part_1(y_min)}")
    print(f"Part 2: {part_2(x_min, x_max, y_min, y_max)}")
