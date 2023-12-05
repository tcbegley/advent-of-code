import sys
from dataclasses import dataclass
from tqdm.auto import tqdm


@dataclass
class MapEntry:
    dest: int
    src: int
    length: int


def parse_block(block):
    _, *block = block.split("\n")
    return [MapEntry(*map(int, row.split(" "))) for row in block]


def load_data(path):
    with open(path) as f:
        seeds, *blocks = f.read().strip().split("\n\n")
    seeds = list(map(int, seeds.split(":")[1].strip().split(" ")))
    maps = [parse_block(block) for block in blocks]
    return seeds, maps


def part_1(seeds, maps):
    numbers = seeds
    for map_ in maps:
        new_numbers = []
        for number in tqdm(numbers):
            for entry in map_:
                if entry.src <= number < entry.src + entry.length:
                    new_numbers.append(entry.dest + (number - entry.src))
                    break
            else:
                new_numbers.append(number)
        numbers = new_numbers
    return min(numbers)


def part_2(seeds, maps):
    new_seeds = []
    for start, length in zip(*([iter(seeds)] * 2)):
        new_seeds.extend(range(start, start + length))

    return part_1(new_seeds, maps)


if __name__ == "__main__":
    seeds, maps = load_data(sys.argv[1])
    print(f"Part 1: {part_1(seeds, maps)}")
    print(f"Part 2: {part_2(seeds, maps)}")
