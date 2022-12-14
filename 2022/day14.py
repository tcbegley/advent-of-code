import sys


def load_data(path):
    def process_line(line):
        return [
            tuple(map(int, coord.split(","))) for coord in line.split(" -> ")
        ]

    with open(path) as f:
        lines = f.read().strip().split("\n")

    return [process_line(line) for line in lines]


def init_cave(rocks):
    cave = {}
    for rock in rocks:
        for (x1, y1), (x2, y2) in zip(rock, rock[1:]):
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    cave[(x1, y)] = "#"
            else:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    cave[(x, y1)] = "#"

    return cave


def drop_sand(cave, hook):
    sand = (500, 0)

    while True:
        if hook(sand, cave):
            return False
        x, y = sand
        if (x, y + 1) not in cave:
            sand = (x, y + 1)
        elif (x - 1, y + 1) not in cave:
            sand = (x - 1, y + 1)
        elif (x + 1, y + 1) not in cave:
            sand = (x + 1, y + 1)
        else:
            cave[sand] = "o"
            return True


def simulate(cave, hook):
    count = 0
    while drop_sand(cave, hook):
        count += 1

    return count


def part_1(rocks):
    cave = init_cave(rocks)
    max_rock = max(y for _, y in cave)
    return simulate(cave, lambda sand, _: sand[1] > max_rock)


def part_2(rocks):
    cave = init_cave(rocks)

    # add the floor
    floor = max(y for _, y in cave) + 2
    for x in range(500 - floor, 500 + floor + 1):
        cave[(x, floor)] = "#"

    return simulate(cave, lambda _, cave: (500, 0) in cave)


if __name__ == "__main__":
    rocks = load_data(sys.argv[1])
    print(f"Part 1: {part_1(rocks)}")
    print(f"Part 2: {part_2(rocks)}")
