import sys


def load_data(path):
    with open(path) as f:
        return [int(n) for n in f.read().strip().split()]


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
    left = 0
    right = 1

    while (x := sum(numbers[left:right])) != target:
        if x < target:
            right += 1
        else:
            left += 1

    return numbers[left:right]


def part_1(numbers, offset=25):
    i = offset

    while check_sum(numbers[i], numbers[i - offset : i]):
        i += 1

    return numbers[i]


def part_2(target, numbers):
    seq = search(target, numbers)
    return min(seq) + max(seq)


if __name__ == "__main__":
    numbers = load_data(sys.argv[1])
    part_1_ans = part_1(numbers)
    print(f"Part 1: {part_1_ans}")
    print(f"Part 2: {part_2(part_1_ans, numbers)}")
