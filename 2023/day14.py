import sys


def load_data(path):
    with open(path) as f:
        return [list(row) for row in f.read().strip().split("\n")]


def tilt(tiles):
    zero_count = dot_count = 0
    for c in tiles:
        if c == "#":
            yield from "O" * zero_count + "." * dot_count
            yield "#"
            zero_count = dot_count = 0
        elif c == "O":
            zero_count += 1
        else:
            dot_count += 1
    yield from "O" * zero_count + "." * dot_count


def cycle(grid):
    n_rows, n_cols = len(grid), len(grid[0])
    for col in range(n_cols):
        for row, char in enumerate(tilt(grid[r][col] for r in range(n_rows))):
            grid[row][col] = char

    for row in range(n_rows):
        for col, char in enumerate(tilt(grid[row][c] for c in range(n_cols))):
            grid[row][col] = char

    for col in range(n_cols):
        for row, char in enumerate(
            tilt(grid[r][col] for r in range(n_rows - 1, -1, -1))
        ):
            grid[n_rows - 1 - row][col] = char

    for row in range(n_rows):
        for col, char in enumerate(
            tilt(grid[row][c] for c in range(n_cols - 1, -1, -1))
        ):
            grid[row][n_cols - 1 - col] = char

    return grid


def format_grid(grid):
    return "\n".join("".join(row) for row in grid)


def total_load(grid):
    n_rows = len(data)
    return sum(n_rows - r for r, row in enumerate(grid) for char in row if char == "O")


def part_1(data):
    # tilt north
    n_rows, n_cols = len(data), len(data[0])
    for col in range(n_cols):
        for row, char in enumerate(tilt(data[r][col] for r in range(n_rows))):
            data[row][col] = char

    return total_load(data)


def part_2(data, n_cycles=1_000_000_000):
    seen = {format_grid(data): 0}
    load = [total_load(data)]
    for i in range(1, n_cycles + 1):
        data = cycle(data)
        state = format_grid(data)
        if state in seen:
            last_seen = seen[state]
            cycle_length = i - last_seen
            return load[(n_cycles - last_seen) % cycle_length + last_seen]
        seen[format_grid(data)] = i
        load.append(total_load(data))


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
