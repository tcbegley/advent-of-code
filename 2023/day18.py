import sys

DIRECTIONS = [(1, 0), (0, -1), (-1, 0), (0, 1)]
DIRECTION_LOOKUP = dict(zip("RDLU", DIRECTIONS))


def process_row(row, part_2):
    direction, steps, colour = row.split(" ")
    if part_2:
        colour = colour.removeprefix("(#").removesuffix(")")
        direction = DIRECTIONS[int(colour[-1])]
        steps = int(colour[:-1], base=16)
    else:
        steps = int(steps)
        direction = DIRECTION_LOOKUP[direction]

    return (direction, steps)


def load_data(path, part_2=False):
    with open(path) as f:
        rows = f.read().strip().split("\n")

    return [process_row(row, part_2=part_2) for row in rows]


def tunnel(data):
    vertices = []
    loc = (0, 0)
    for direction, steps in data:
        loc = (loc[0] + steps * direction[0], loc[1] + steps * direction[1])
        vertices.append(loc)

    return vertices


def collect_vertices(data):
    vertices = sorted(tunnel(data))
    out = []
    current_x = None
    for vertex in vertices:
        if vertex[0] != current_x:
            out.append([])
            current_x = vertex[0]
        out[-1].append(vertex)
    return out


def merge_intervals(current, incoming):
    for interval in incoming:
        current = merge(current, interval)
    return current


def merge(current, interval):
    future = []
    idx = 0
    # keep all intervals to left of this one
    while idx < len(current) and current[idx][1] < interval[0]:
        future.append(current[idx])
        idx += 1

    if idx >= len(current) or current[idx][0] > interval[1]:
        future.append(interval)
    elif current[idx][0] == interval[1]:
        future.append((interval[0], current[idx][1]))
        idx += 1
    elif current[idx][0] == interval[0]:
        if interval[1] < current[idx][1]:
            future.append((interval[1], current[idx][1]))
        idx += 1
    elif current[idx][0] < interval[0]:
        if interval[1] < current[idx][1]:
            future.extend(
                [(current[idx][0], interval[0]), (interval[1], current[idx][1])]
            )
        elif interval[1] == current[idx][1]:
            future.append((current[idx][0], interval[0]))
        elif interval[0] == current[idx][1]:
            if idx + 1 < len(current) and current[idx + 1][0] == interval[1]:
                future.append((current[idx][0], current[idx + 1][1]))
                idx += 1
            else:
                future.append((current[idx][0], interval[1]))
        idx += 1

    future.extend(current[idx:])
    return future


def merge_overlapping(intervals):
    intervals.sort()
    merged_intervals = []

    for interval in intervals:
        if merged_intervals and merged_intervals[-1][1] >= interval[0]:
            merged_intervals[-1] = (
                merged_intervals[-1][0],
                max(merged_intervals[-1][1], interval[1]),
            )
        else:
            merged_intervals.append(interval)

    return merged_intervals


def total_length(intervals):
    return sum(b - a + 1 for a, b in intervals)


def solve(data):
    vertices = collect_vertices(data)
    current = []
    total = 0
    for i, row in enumerate(vertices):
        next_ = merge_intervals(
            current, [(y1, y2) for (_, y1), (_, y2) in zip(*[iter(row)] * 2)]
        )
        total += total_length(merge_overlapping(current + next_))
        if next_:
            total += total_length(next_) * (vertices[i + 1][0][0] - row[0][0] - 1)
        current = next_

    return total


def part_2(data):
    return list(tunnel(data))


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {solve(data)}")
    data = load_data(sys.argv[1], part_2=True)
    print(f"Part 2: {solve(data)}")
