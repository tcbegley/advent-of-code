import sys


def load_data(path):
    with open(path) as f:
        lines = f.readlines()

    east = set()
    south = set()

    for y, row in enumerate(lines):
        for x, c in enumerate(row.strip()):
            if c == ">":
                east.add((x, y))
            elif c == "v":
                south.add((x, y))

    max_y, max_x = len(lines), len(lines[0].strip())
    return east, south, max_x, max_y


def iterate(east, south, max_x, max_y):
    occupied = east | south
    new_east = {
        ((x + 1) % max_x, y)
        if ((x + 1) % max_x, y) not in occupied
        else (x, y)
        for x, y in east
    }
    occupied = new_east | south
    new_south = {
        (x, (y + 1) % max_y)
        if (x, (y + 1) % max_y) not in occupied
        else (x, y)
        for (x, y) in south
    }
    return new_east, new_south


def part_1(east, south, max_x, max_y):
    count = 0
    while True:
        new_east, new_south = iterate(east, south, max_x, max_y)
        count += 1

        if new_east == east and new_south == south:
            break

        east, south = new_east, new_south

    return count


if __name__ == "__main__":
    east, south, max_x, max_y = load_data(sys.argv[1])
    print(f"Part 1: {part_1(east, south, max_x, max_y)}")
