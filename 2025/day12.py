import sys


def rotate(shape):
    lookup = {
        (0, 0): (0, 2),
        (0, 1): (1, 2),
        (0, 2): (2, 2),
        (1, 0): (0, 1),
        (1, 1): (1, 1),
        (1, 2): (2, 1),
        (2, 0): (0, 0),
        (2, 1): (1, 0),
        (2, 2): (2, 0),
    }
    return tuple(sorted(lookup[loc] for loc in shape))


def flip(shape):
    lookup = {
        (0, 0): (0, 2),
        (0, 1): (0, 1),
        (0, 2): (0, 0),
        (1, 0): (1, 2),
        (1, 1): (1, 1),
        (1, 2): (1, 0),
        (2, 0): (2, 2),
        (2, 1): (2, 1),
        (2, 2): (2, 0),
    }
    return tuple(sorted(lookup[loc] for loc in shape))


def process_shape(shape):
    shape = tuple(
        (r, c)
        for r, row in enumerate(shape.split("\n")[1:])
        for c, val in enumerate(row)
        if val == "#"
    )
    variants = {shape, flip(shape)}
    for _ in range(3):
        shape = rotate(shape)
        variants.add(shape)
        variants.add(flip(shape))

    return variants


def process_size(size):
    dims, counts = size.split(": ")
    dims = tuple(map(int, dims.split("x")))
    counts = tuple(map(int, counts.split(" ")))
    return dims, counts


def load_data(path):
    with open(path) as f:
        *shapes, sizes = f.read().strip().split("\n\n")

    shapes = [process_shape(shape) for shape in shapes]
    sizes = [process_size(size) for size in sizes.split("\n")]
    return shapes, sizes


def part_1(data):
    return data


def part_2(data):
    pass


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
