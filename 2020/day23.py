import sys

from tqdm.auto import tqdm


def load_data(path):
    with open(path) as f:
        return tuple(map(int, f.read().strip()))


def print_numbers(numbers):
    current = next(iter(numbers))
    out = []

    for _ in range(len(numbers)):
        out.append(current)
        current = numbers[current]["r"]

    return out


def play_game(numbers, moves=100):
    n = len(numbers)
    current = numbers[0]

    numbers = {
        num: {"l": numbers[i - 1], "r": numbers[(i + 1) % n]}
        for i, num in enumerate(numbers)
    }

    for i in tqdm(range(moves), leave=False):
        current_slice = []
        cur = current
        for _ in range(3):
            cur = numbers[cur]["r"]
            current_slice.append(cur)

        slice_left = numbers[current_slice[0]]["l"]
        slice_right = numbers[current_slice[-1]]["r"]
        numbers[slice_left]["r"] = slice_right
        numbers[slice_right]["l"] = slice_left

        target = current - 1

        while target in current_slice or not (1 <= target <= n):
            if target < 1:
                target = n
            else:
                target -= 1

        target_right = numbers[target]["r"]
        numbers[target]["r"] = current_slice[0]
        numbers[target_right]["l"] = current_slice[-1]
        numbers[current_slice[0]]["l"] = target
        numbers[current_slice[-1]]["r"] = target_right

        current = numbers[current]["r"]

    return numbers


def part_1(numbers):
    numbers = play_game(numbers)
    current = 1
    out = []

    for _ in range(len(numbers)):
        out.append(current)
        current = numbers[current]["r"]

    return "".join(map(str, out[1:]))


def part_2(numbers):
    numbers = play_game(numbers + tuple(range(10, 1_000_001)), moves=10_000_000)
    return (x := numbers[1]["r"]) * numbers[x]["r"]


if __name__ == "__main__":
    numbers = load_data(sys.argv[1])
    print(f"Part 1: {part_1(numbers)}")
    print(f"Part 2: {part_2(numbers)}")
