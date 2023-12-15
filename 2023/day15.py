import sys


def load_data(path):
    with open(path) as f:
        return f.read().strip().split(",")


def h(s):
    value = 0
    for c in s:
        value = 17 * (ord(c) + value) % 256
    return value


def part_1(data):
    return sum(h(s) for s in data)


def part_2(data):
    hashmap = [[] for _ in range(256)]
    for instruction in data:
        if instruction.endswith("-"):
            # delete
            label = instruction[:-1]
            idx = h(label)
            hashmap[idx] = [item for item in hashmap[idx] if item[0] != label]
        else:
            # insert
            label, value = instruction.split("=")
            idx, value = h(label), int(value)
            for item in hashmap[idx]:
                if item[0] == label:
                    item[1] = value
                    break
            else:
                hashmap[idx].append([label, value])

    return sum(
        box_num * slot_num * value
        for box_num, box in enumerate(hashmap, start=1)
        for slot_num, (_, value) in enumerate(box, start=1)
    )


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
