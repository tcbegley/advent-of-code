import sys


def load_data(path):
    with open(path) as f:
        return [
            int(row)
            for row in f.read().strip().replace("L", "-").replace("R", "+").split("\n")
        ]


def part_1(data):
    cur = 50
    count = 0

    for rot in data:
        cur = (cur + rot) % 100
        if cur == 0:
            count += 1

    return count


def part_2(data):
    cur = 50
    count = 0

    for rot in data:
        start = cur
        turns, cur = divmod(cur + rot, 100)

        if turns >= 0:
            # don't double count the final zero if we stop on it
            count += max(turns - (cur == 0), 0)
        else:
            # if we turned left, don't count the initial zero if it was there
            count += abs(turns) - (start == 0)

        # if we stopped on a zero, count it
        count += cur == 0

    return count


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
