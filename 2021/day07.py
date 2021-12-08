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
    def cost(position):
        return sum(
            ((p - position) ** 2 + abs(p - position)) // 2 for p in positions
        )

    # can prove that best position is always within distance 1 of the mean
    # hence take integer part of mean and add 1 to check integers either side
    # of the mean
    mean = int(sum(positions) / len(positions))
    return min(cost(mean), cost(mean + 1))


if __name__ == "__main__":
    positions = load_data(sys.argv[1])
    print(f"Part 1: {part_1(positions)}")
    print(f"Part 2: {part_2(positions)}")
