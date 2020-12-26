import json
import sys


def load_data(path):
    with open(path) as f:
        return json.load(f)


def rec_sum(obj, ignore_red=False):
    if isinstance(obj, (int, float)):
        return obj
    if isinstance(obj, list):
        return sum(rec_sum(o, ignore_red) for o in obj)
    elif isinstance(obj, dict):
        if ignore_red and "red" in obj.values():
            return 0
        return sum(rec_sum(o, ignore_red) for o in obj.values())
    else:
        # anything else we encounter can't contribute to the sum
        return 0


def part_1(doc):
    return rec_sum(doc)


def part_2(doc):
    return rec_sum(doc, ignore_red=True)


if __name__ == "__main__":
    doc = load_data(sys.argv[1])
    print(f"Part 1: {part_1(doc)}")
    print(f"Part 2: {part_2(doc)}")
