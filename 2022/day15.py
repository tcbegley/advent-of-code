import re
import sys

NUMBER_PATTERN = re.compile(r"-?\d+")


def load_data(path):
    with open(path) as f:
        return [
            ((int(sx), int(sy)), (int(bx), int(by)))
            for sx, sy, bx, by in map(
                NUMBER_PATTERN.findall, f.read().strip().split("\n")
            )
        ]


def l1(x1, x2):
    return sum(abs(a - b) for a, b in zip(x1, x2))


def blocked_positions(sensor, beacon, y):
    dist = l1(sensor, beacon)
    x_dist = dist - abs(sensor[1] - y)
    left = sensor[0] - x_dist
    right = sensor[0] + x_dist
    if left <= right:
        return (left, right)
    return None


def merge_intervals(intervals):
    intervals = [i for i in intervals if i is not None]
    intervals = sorted(intervals, key=lambda i: i[0])
    min_overlap = float("inf")

    new_intervals = [intervals[0]]
    for i in intervals[1:]:
        prev = new_intervals[-1]
        if prev[1] < i[0]:
            new_intervals.append(i)
        else:
            new_intervals[-1] = (prev[0], max(prev[1], i[1]))
            min_overlap = min(min_overlap, prev[1] - i[0])

    return new_intervals, min_overlap


def is_in(val, intervals):
    return any(i[0] <= val <= i[1] for i in intervals)


def part_1(data, y=2_000_000):
    intervals = [blocked_positions(sensor, beacon, y) for sensor, beacon in data]
    beacons = {(bx, by) for _, (bx, by) in data}
    sensors = {(sx, sy) for (sx, sy), _ in data}

    intervals, _ = merge_intervals(intervals)
    offset = sum(is_in(sx, intervals) for (sx, sy) in sensors if sy == y) + sum(
        is_in(bx, intervals) for (bx, by) in beacons if by == y
    )
    return sum(i[1] - i[0] + 1 for i in intervals) - offset


def part_2(data):
    y = 0
    while True:
        intervals, min_overlap = merge_intervals(
            [blocked_positions(sensor, beacon, y) for sensor, beacon in data]
        )
        if len(intervals) > 1:
            return (intervals[0][1] + 1) * 4_000_000 + y
        else:
            y += max(
                1,
                min(
                    abs(intervals[0][0]),
                    intervals[0][1] - 4_000_000,
                    min_overlap // 2,
                ),
            )


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
