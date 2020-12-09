import sys


def check_sum(n, lst):
    mn = min(lst)
    mx = max(lst)

    for i in range(len(lst)):
        x = lst[i]
        if n - x > mx or n - x < mn:
            continue
        for j in range(i + 1, len(lst)):
            y = lst[j]
            if x + y == n:
                return True

    return False


def search(target, numbers):
    l = 0
    r = 1

    while (x := sum(numbers[l:r])) != target:
        if x < target:
            r += 1
        else:
            l += 1

    return numbers[l:r]


def answer(path):
    with open(path) as f:
        numbers = [int(n) for n in f.read().strip().split()]

    i = 25

    while check_sum(numbers[i], numbers[i-25:i]):
        i += 1

    target = numbers[i]
    seq = search(target, numbers)

    return min(seq) + max(seq)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
