def redistribute(a):
    n = len(a)
    m = max(a)
    start = a.index(m)
    a[start] = 0
    for i in range(start + 1, start + m + 1):
        a[i % n] += 1


def answer(file_path):
    with open(file_path, "r") as f:
        a = list(map(int, f.read().strip().split("\t")))
    cache = {}
    count = 0
    while True:
        redistribute(a)
        count += 1
        if tuple(a) in cache:
            break
        cache[tuple(a)] = count
    return count - cache[tuple(a)]


if __name__ == "__main__":
    print(answer("input/6.txt"))
