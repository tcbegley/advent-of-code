import sys


def process_size(size):
    dims, counts = size.split(": ")
    dims = tuple(map(int, dims.split("x")))
    counts = tuple(map(int, counts.split(" ")))
    return dims, counts


def load_data(path):
    with open(path) as f:
        *shapes, sizes = f.read().strip().split("\n\n")

    shape_sizes = [shape.count("#") for shape in shapes]
    sizes = [process_size(size) for size in sizes.split("\n")]
    return shape_sizes, sizes


def check_valid(shape_sizes, size):
    (w, h), counts = size
    combined_size = sum(
        count * shape_size for count, shape_size in zip(counts, shape_sizes)
    )
    if (w // 3) * (h // 3) >= sum(counts):
        return True
    elif combined_size >= w * h:
        return False

    # this problem is hard in general, but if we never hit this error then the cases
    # we've been given are all obvious (either total area taken up by presents exceeds
    # the size of the grid, or the grid fits the required number of 3x3 boxes without
    # accounting for the actual shape)
    raise RuntimeError


def part_1(shape_sizes, sizes):
    return sum(check_valid(shape_sizes, size) for size in sizes)


if __name__ == "__main__":
    shape_sizes, sizes = load_data(sys.argv[1])
    print(f"Part 1: {part_1(shape_sizes, sizes)}")
