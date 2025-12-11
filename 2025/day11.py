import sys
from functools import cache


def load_data(path):
    with open(path) as f:
        rows = f.read().strip().split("\n")

    data = {}
    for row in rows:
        key, values = row.split(": ")
        data[key] = values.split(" ")

    return data


def part_1(data):
    @cache
    def count_paths(node):
        if node == "out":
            return 1

        return sum(count_paths(child) for child in data[node])

    return count_paths("you")


def part_2(data):
    @cache
    def count_paths(node, visited_dac, visited_fft):
        if node == "out" and visited_dac and visited_fft:
            return 1

        return sum(
            count_paths(
                child, visited_dac or child == "dac", visited_fft or child == "fft"
            )
            for child in data.get(node, [])
        )

    return count_paths("svr", False, False)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
