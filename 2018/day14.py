import sys


def load_data(path):
    with open(path) as f:
        return int(f.read().strip())


def digits(n):
    for d in str(n):
        yield int(d)


def solve(hook):
    elf1, elf2 = 0, 1
    recipes = [3, 7]

    while True:
        recipes.extend(digits(recipes[elf1] + recipes[elf2]))
        elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
        elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)

        if (res := hook(recipes)) is not None:
            return res


def part_1(n):
    def hook(recipes):
        if len(recipes) < n + 10:
            return None
        return "".join(map(str, recipes[n : n + 10]))

    return solve(hook)


def part_2(n):
    target = list(digits(n))

    def hook(recipes):
        if target == recipes[-6:]:
            return len(recipes) - 6
        elif target == recipes[-7:-1]:
            return len(recipes) - 7
        return None

    return solve(hook)


if __name__ == "__main__":
    n = load_data(sys.argv[1])
    print(f"Part 1: {part_1(n)}")
    print(f"Part 2: {part_2(n)}")
