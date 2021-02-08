import hashlib
import sys


def load_data(path):
    with open(path) as f:
        return f.read().strip()


def generate_password(key, position=False):
    prefix = "0" * 5
    i = 0
    count = 0
    password = [None] * 8
    while count < 8:
        hash_ = hashlib.md5(f"{key}{i}".encode())
        if (h := hash_.hexdigest()).startswith(prefix):
            if position:
                if (loc := h[5]) in "01234567":
                    if password[int(loc)] is None:
                        password[int(loc)] = h[6]
                        count += 1
            else:
                password[count] = h[5]
                count += 1
        i += 1
    return "".join(password)


def part_1(key):
    return generate_password(key)


def part_2(key):
    return generate_password(key, True)


if __name__ == "__main__":
    key = load_data(sys.argv[1])
    print(f"Part 1: {part_1(key)}")
    print(f"Part 2: {part_2(key)}")
