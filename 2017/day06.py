import sys


def load_data(path):
    with open(path, "r") as f:
        return [int(i) for i in f.read().strip().split("\t")]


def redistribute(memory_banks):
    blocks, n_banks = max(memory_banks), len(memory_banks)
    start = memory_banks.index(blocks)
    memory_banks[start] = 0
    for i in range(start + 1, start + blocks + 1):
        memory_banks[i % n_banks] += 1


def count_redistributions(memory_banks):
    cache, count = {}, 0

    while True:
        redistribute(memory_banks)
        count += 1
        if (state := tuple(memory_banks)) in cache:
            break
        cache[state] = count

    return count, cache[state]


if __name__ == "__main__":
    memory_banks = load_data(sys.argv[1])
    count, last_seen = count_redistributions(memory_banks)
    print(f"Part 1: {count}")
    print(f"Part 2: {count - last_seen}")
