import re
import sys

NUMBER_PATTERN = re.compile(r"\d+")
PART_2_OFFSET = 10_000_000_000_000


def parse_block(block):
    ax, ay, bx, by, px, py = map(int, NUMBER_PATTERN.findall(block))
    return (ax, bx, ay, by), (px, py)


def load_data(path):
    with open(path) as f:
        return [parse_block(block) for block in f.read().strip().split("\n\n")]


def solve(mat, prize):
    # 2d linear system, check if matrix is invertible then invert using the formula
    ax, bx, ay, by = mat
    det = ax * by - bx * ay
    if det == 0:
        return None

    px, py = prize
    # we only care about integer solutions, so integer divide
    a = (by * px - bx * py) // det
    b = (ax * py - ay * px) // det

    # and then check whether it's still a solution
    if a * ax + b * bx != px or a * ay + b * by != py:
        return None

    return a, b


def total_cost(data, offset=0):
    cost = 0
    for mat, prize in data:
        prize = (prize[0] + offset, prize[1] + offset)
        if (solution := solve(mat, prize)) is not None:
            a, b = solution
            cost += 3 * a + b
    return cost


def part_1(data):
    return total_cost(data)


def part_2(data):
    return total_cost(data, offset=PART_2_OFFSET)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
