import sys


class Elf:
    def __init__(self, loc, recipe):
        self.loc = loc
        self.recipe = recipe


def answer(n):
    recipes = [3, 7]
    elf1 = Elf(0, 3)
    elf2 = Elf(1, 7)

    while len(recipes) < n + 10:
        recipes.extend([int(i) for i in str(elf1.recipe + elf2.recipe)])
        elf1.loc = (elf1.loc + 1 + elf1.recipe) % len(recipes)
        elf1.recipe = recipes[elf1.loc]
        elf2.loc = (elf2.loc + 1 + elf2.recipe) % len(recipes)
        elf2.recipe = recipes[elf2.loc]

    return "".join(str(i) for i in recipes[n : n + 10])


if __name__ == "__main__":
    print(answer(int(sys.argv[1])))
