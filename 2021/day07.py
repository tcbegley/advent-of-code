import sys


def load_data(path):
    with open(path) as f:
        return [int(n) for n in f.read().strip().split(",")]


def part_1(positions):
    positions = sorted(positions)
    n = len(positions)
    med = positions[n // 2]
    return sum(abs(pos - med) for pos in positions)


def part_2(positions):
    # We have a triangular cost function which is approximately quadratic,
    # hence the answer will be close to the mean

    # the gradient wrt the position _at the mean_ is

    # 0.5 * sgn(\bar{x} - x_i)

    # this is negative if there are more x_i's greater than the mean than there
    # are x_i's less than the mean. hence to decrease the loss we should test
    # positions greater than the mean in the former case, and less than the
    # mean in the latter case. We know that the cost is convex, so we can just
    # test positions incrementing / decrementing by 1 each time until we see
    # the first increase in cost.
    def cost(position):
        return sum(
            ((p - position) ** 2 + abs(p - position)) // 2 for p in positions
        )

    mean = int(sum(positions) / len(positions))

    min_cost = cost(mean)
    if sum(p > mean for p in positions) >= 0:
        step = 1
    else:
        step = -1

    position = mean + step

    while (new_cost := cost(position)) < min_cost:
        min_cost = new_cost
        position += step

    return min_cost


if __name__ == "__main__":
    positions = load_data(sys.argv[1])
    print(f"Part 1: {part_1(positions)}")
    print(f"Part 2: {part_2(positions)}")
