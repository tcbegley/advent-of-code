import sys


def process_range(range_):
    start, end = range_.split("-")
    return (int(start), int(end))


def load_data(path):
    with open(path) as f:
        return [process_range(range_) for range_ in f.read().strip().split(",")]


def n_digits(n):
    return len(str(n))


def repeat(val, times):
    shift = 10 ** n_digits(val)
    ret = 0
    for _ in range(times):
        ret = ret * shift + val
    return ret


def list_invalid_ids(start, end, n_repeats=2):
    start_digits, end_digits = n_digits(start), n_digits(end)
    if start_digits < end_digits:
        # if different number of digits, create two new synthetic ranges and recursively
        # apply to those
        mid = 10**start_digits
        return list_invalid_ids(start, mid - 1, n_repeats) + list_invalid_ids(
            mid, end, n_repeats
        )
    return _list_invalid(start, end, n_repeats)


def _list_invalid(start, end, n_repeats):
    if (n := n_digits(start)) == 1 or n % n_repeats != 0:
        return []

    seq_length = n // n_repeats
    val = start_val = int(str(start)[:seq_length])
    ids = []
    while val < 10**seq_length:
        if start <= (id_ := repeat(val, n // seq_length)) <= end:
            ids.append(id_)
        elif val != start_val:
            break
        val += 1
    return ids


def part_1(data):
    total = 0
    for start, end in data:
        ids_ = list_invalid_ids(start, end)
        total += sum(ids_)

    return total


def part_2(data):
    total = 0
    for start, end in data:
        invalid = set()
        for n_repeats in range(2, n_digits(end) + 1):
            invalid.update(list_invalid_ids(start, end, n_repeats))
        total += sum(invalid)

    return total


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
