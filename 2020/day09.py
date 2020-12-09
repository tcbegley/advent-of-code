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


def answer(path):
    with open(path) as f:
        numbers = [int(n) for n in f.read().strip().split()]

    i = 25

    while check_sum(numbers[i], numbers[i - 25 : i]):
        i += 1

    return numbers[i]


if __name__ == "__main__":
    print(answer(sys.argv[1]))
