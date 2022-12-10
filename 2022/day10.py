import sys


def load_data(path):
    with open(path) as f:
        return f.read().strip().split("\n")


def register_value(data):
    register = 1

    for cmd in data:
        yield register
        if cmd[:4] == "addx":
            yield register
            register += int(cmd[5:])


def part_1(data):
    total = 0
    targets = {20, 60, 100, 140, 180, 220}

    for cycle, register in enumerate(register_value(data), start=1):
        if cycle in targets:
            total += cycle * register

    return total


def part_2(data):
    pixels = []
    for cycle, register in enumerate(register_value(data), start=1):
        if register <= (cycle - 1) % 40 + 1 <= register + 2:
            pixels.append("#")
        else:
            pixels.append(".")

    return "\n" + "\n".join(
        "".join(pixels[i : i + 40]) for i in range(0, 240, 40)
    )


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
