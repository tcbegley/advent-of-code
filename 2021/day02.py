import sys


def load_data(path):
    def parse_line(line):
        cmd, num = line.strip().split(" ")
        return cmd, int(num)

    with open(path) as f:
        return [parse_line(line) for line in f.readlines()]


def part_1(directions):
    horizontal, depth = 0, 0
    for cmd, num in directions:
        if cmd == "forward":
            horizontal += num
        elif cmd == "down":
            depth += num
        elif cmd == "up":
            depth -= num
    return horizontal * depth


def part_2(directions):
    horizontal, depth, aim = 0, 0, 0
    for cmd, num in directions:
        if cmd == "forward":
            horizontal += num
            depth += num * aim
        elif cmd == "down":
            aim += num
        elif cmd == "up":
            aim -= num
    return horizontal * depth


if __name__ == "__main__":
    directions = load_data(sys.argv[1])
    print(f"Part 1: {part_1(directions)}")
    print(f"Part 2: {part_2(directions)}")
