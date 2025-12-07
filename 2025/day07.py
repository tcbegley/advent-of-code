import sys
from collections import Counter


def load_data(path):
    with open(path) as f:
        return [
            {i for i, c in enumerate(row) if c in "S^"}
            for row in f.read().strip().split("\n")[::2]
        ]


def simulate(data):
    beams = {beam: 1 for beam in data[0]}
    splits = 0

    for row in data[1:]:
        new_beams = Counter()
        for beam, count in beams.items():
            if beam in row:
                new_beams[beam - 1] += count
                new_beams[beam + 1] += count
                splits += 1
            else:
                new_beams[beam] += count
        beams = new_beams

    return splits, sum(beams.values())


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    splits, total_paths = simulate(data)
    print(f"Part 1: {splits}")
    print(f"Part 2: {total_paths}")
