import sys

try:
    from tqdm.auto import tqdm
except ModuleNotFoundError:

    def tqdm(iterator, **kwargs):
        return iterator


def load_data(path):
    with open(path) as f:
        return [int(i) for i in f.read().strip().split(",")]


def play_game(numbers, iterations=2020):
    game = {}
    next_number = 0
    for i in tqdm(range(iterations), leave=False):
        if i < len(numbers):
            game[numbers[i]] = i
        else:
            number = next_number
            if number in game:
                next_number = i - game[next_number]
            else:
                next_number = 0
            game[number] = i

    return number


def part_1(numbers):
    return play_game(numbers)


def part_2(numbers):
    return play_game(numbers, 30000000)


if __name__ == "__main__":
    numbers = load_data(sys.argv[1])
    print(f"Part 1: {part_1(numbers)}")
    print(f"Part 2: {part_2(numbers)}")
