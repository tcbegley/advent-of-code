import sys


def answer(path):
    with open(path) as f:
        steps = [int(i) for i in f.read().strip().split("\n")]
    seen, total, i, n = set(), 0, 0, len(steps)
    while True:
        if total in seen:
            return total
        seen.add(total)
        total += steps[i % n]
        i += 1


if __name__ == "__main__":
    print(answer(sys.argv[1]))
