import sys


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


def answer(file_path):
    with open(file_path, "r") as f:
        lengths = list(map(int, f.read().strip().split(",")))
    w = WrappedList(list(range(256)))
    skip = 0
    pos = 0
    for l in lengths:
        if l > 1:
            w[pos : pos + l] = list(reversed(w[pos : pos + l]))
        pos += l + skip
        skip += 1
    return w[0] * w[1]


if __name__ == "__main__":
    print(answer(sys.argv[1]))
