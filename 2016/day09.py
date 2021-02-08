import sys


def load_data(path):
    with open(path) as f:
        return f.read().strip()


def decompress(characters):
    result = ""
    left, right = 0, 0

    while "(" in characters[left:]:
        left = characters[left:].index("(") + left
        result += characters[right:left]

        right = left + 1
        right = characters[right:].index(")") + right

        n_chars, repeat = map(int, characters[left + 1 : right].split("x"))
        result += characters[right + 1 : right + n_chars + 1] * repeat

        left, right = right + n_chars + 1, right + n_chars + 1

    result += characters[right:]

    return result


def decompressed_length(characters):
    total = 0
    left, right = 0, 0

    while "(" in characters[left:]:
        left = characters[left:].index("(") + left
        total += right - left

        right = left + 1
        right = characters[right:].index(")") + right

        n_chars, repeat = map(int, characters[left + 1 : right].split("x"))

        total += (
            decompressed_length(characters[right + 1 : right + n_chars + 1])
            * repeat
        )

        left, right = right + n_chars + 1, right + n_chars + 1

    total += len(characters) - right

    return total


def part_1(characters):
    return len(decompress(characters))


def part_2(characters):
    return decompressed_length(characters)


if __name__ == "__main__":
    characters = load_data(sys.argv[1])
    print(f"Part 1: {part_1(characters)}")
    print(f"Part 2: {part_2(characters)}")
