import sys

KEY = 811589153


def load_data(path):
    with open(path) as f:
        return [int(n) for n in f.read().strip().split("\n")]


def mix(data, indices, index_lookup):
    n = len(data)
    for i in range(n):
        # get the current position of the ith entry of data
        loc = index_lookup[i]
        # n - 1 because position 0 in the list is the same as n - 1!
        new_loc = (loc + data[i]) % (n - 1)
        if loc < new_loc:
            for j in range(loc, new_loc):
                indices[j] = indices[j + 1]
                index_lookup[indices[j]] = j
        elif new_loc < loc:
            for j in range(loc, new_loc, -1):
                indices[j] = indices[j - 1]
                index_lookup[indices[j]] = j
        indices[new_loc] = i
        index_lookup[i] = new_loc


def get_answer(data, indices, index_lookup):
    n = len(data)
    idx = index_lookup[data.index(0)]
    return (
        data[indices[(idx + 1000) % n]]
        + data[indices[(idx + 2000) % n]]
        + data[indices[(idx + 3000) % n]]
    )


def part_1(data):
    n = len(data)
    # the current arrangement of indices into data
    indices = list(range(n))
    # lookup for current position of a given index
    index_lookup = {i: i for i in range(n)}

    mix(data, indices, index_lookup)
    return get_answer(data, indices, index_lookup)


def part_2(data):
    data = [value * KEY for value in data]
    n = len(data)
    indices = list(range(n))
    index_lookup = {i: i for i in range(n)}

    for _ in range(10):
        mix(data, indices, index_lookup)

    return get_answer(data, indices, index_lookup)


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
