import sys
from functools import reduce


def load_data(path):
    with open(path) as f:
        return sorted(map(int, f.read().strip().split("\n")), reverse=True)


def pack(weights, target, packed=(), max_length=float("inf"), qe=float("inf")):
    if packed and len(packed) > max_length:
        return None

    packed_sum = sum(packed)
    for i, weight in enumerate(weights):
        if weight == target - packed_sum:
            solution = packed + (weight,)
            if len(solution) < max_length or (
                len(solution) == max_length
                and reduce(lambda a, b: a * b, solution) < qe
            ):
                return solution
        elif weight < target - packed_sum:
            res = pack(
                weights[i + 1 :], target, packed + (weight,), max_length, qe
            )
            if res is not None:
                return res
    return None


def find_best_qe(weights, target):
    max_length, qe = float("inf"), float("inf")

    while candidate := pack(weights, target, max_length=max_length, qe=qe):
        max_length = len(candidate)
        qe = reduce(lambda a, b: a * b, candidate)

    return qe


def part_1(weights):
    return find_best_qe(weights, sum(weights) // 3)


def part_2(weights):
    return find_best_qe(weights, sum(weights) // 4)


if __name__ == "__main__":
    weights = load_data(sys.argv[1])
    print(f"Part 1: {part_1(weights)}")
    print(f"Part 2: {part_2(weights)}")
