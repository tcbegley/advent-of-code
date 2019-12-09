import sys
from functools import reduce


class WrappedList:
    def __init__(self, lst):
        self.l = lst[:]
        self.n = len(lst)

    def __getitem__(self, i):
        if isinstance(i, slice):
            start = i.start % self.n
            stop = i.stop % self.n
            if start >= stop:
                return self.l[start:] + self.l[:stop]
            return self.l[start:stop]
        return self.l[i % self.n]

    def __setitem__(self, i, v):
        if isinstance(i, slice):
            start = i.start % self.n
            stop = i.stop % self.n
            if start >= stop:
                self.l[start:] = v[: self.n - start]
                self.l[:stop] = v[self.n - start :]
            else:
                self.l[start:stop] = v
        else:
            self.l[i % self.n] = v


def densify(nums):
    return reduce(lambda x, y: x ^ y, nums)


def answer(file_path):
    with open(file_path, "r") as f:
        lengths = list(map(ord, f.read().strip())) + [17, 31, 73, 47, 23]
    w = WrappedList(list(range(256)))
    skip = 0
    pos = 0
    for _ in range(64):
        for l in lengths:
            if l > 1:
                w[pos : pos + l] = list(reversed(w[pos : pos + l]))
            pos += l + skip
            skip += 1
    dense = [densify(w[16 * i : 16 * (i + 1)]) for i in range(16)]
    return "".join([hex(x)[2:].zfill(2) for x in dense])


if __name__ == "__main__":
    print(answer(sys.argv[1]))
