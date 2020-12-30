import sys
from functools import reduce


class WrappedList:
    def __init__(self, list_):
        self.list_ = list_[:]
        self.n = len(list_)

    def __getitem__(self, i):
        if isinstance(i, slice):
            start = i.start % self.n
            stop = i.stop % self.n
            if start >= stop:
                return self.list_[start:] + self.list_[:stop]
            return self.list_[start:stop]
        return self.list_[i % self.n]

    def __setitem__(self, i, v):
        if isinstance(i, slice):
            start = i.start % self.n
            stop = i.stop % self.n
            if start >= stop:
                self.list_[start:] = v[: self.n - start]
                self.list_[:stop] = v[self.n - start :]
            else:
                self.list_[start:stop] = v
        else:
            self.list_[i % self.n] = v


def load_data(path):
    with open(path) as f:
        return f.read().strip()


def densify(nums):
    return reduce(lambda x, y: x ^ y, nums)


def part_1(string):
    lengths = [int(i) for i in string.split(",")]

    w = WrappedList(list(range(256)))
    skip, pos = 0, 0

    for length in lengths:
        if length > 1:
            w[pos : pos + length] = list(reversed(w[pos : pos + length]))
        pos += length + skip
        skip += 1

    return w[0] * w[1]


def part_2(string):
    lengths = [ord(c) for c in string] + [17, 31, 73, 47, 23]

    w = WrappedList(list(range(256)))
    skip, pos = 0, 0

    for _ in range(64):
        for length in lengths:
            if length > 1:
                w[pos : pos + length] = list(reversed(w[pos : pos + length]))
            pos += length + skip
            skip += 1
    dense = [densify(w[16 * i : 16 * (i + 1)]) for i in range(16)]
    return "".join([hex(x)[2:].zfill(2) for x in dense])


if __name__ == "__main__":
    string = load_data(sys.argv[1])
    print(f"Part 1: {part_1(string)}")
    print(f"Part 2: {part_2(string)}")
