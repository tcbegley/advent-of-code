import sys


class Elf:
    def __init__(self, loc, recipe):
        self.loc = loc
        self.recipe = recipe


def answer(n):
    recipes = "37"
    elf1 = Elf(0, 3)
    elf2 = Elf(1, 7)

    while True:
        current_length = len(recipes)
        recipes += "".join(i for i in str(elf1.recipe + elf2.recipe))
        elf1.loc = (elf1.loc + 1 + elf1.recipe) % len(recipes)
        elf1.recipe = int(recipes[elf1.loc])
        elf2.loc = (elf2.loc + 1 + elf2.recipe) % len(recipes)
        elf2.recipe = int(recipes[elf2.loc])

        end = recipes[max(current_length - 10, 0) :]

        if n in end:
            return end.index(n) + max(current_length - 10, 0)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
