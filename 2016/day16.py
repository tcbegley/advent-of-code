import sys


def load_data(path):
    with open(path) as f:
        return f.read().strip()


def modify(data):
    a = data
    b = "".join("1" if c == "0" else "0" for c in reversed(data))
    return f"{a}0{b}"


def checksum(data):
    return "".join(
        "1" if data[i] == data[i + 1] else "0" for i in range(0, len(data), 2)
    )


def answer(data, n=272):
    while len(data) < n:
        data = modify(data)

    data = data[:n]

    while len(data) % 2 == 0:
        data = checksum(data)

    return data


def part_1(data):
    return answer(data)


def part_2(data):
    return answer(data, n=35651584)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
