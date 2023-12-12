import re
import sys

PATTERN = re.compile(r"([\w ]+) \(contains ([\w, ]+)\)")


def load_data(path):
    with open(path) as f:
        foods = f.read().strip().split("\n")

    return [
        (
            (m := PATTERN.fullmatch(food)).group(1).split(" "),
            m.group(2).split(", "),
        )
        for food in foods
    ]


def isolate_allergens(foods):
    allergens = {}
    for ingredients, contains in foods:
        for allergen in contains:
            if allergen in allergens:
                allergens[allergen] = allergens[allergen].intersection(set(ingredients))
            else:
                allergens[allergen] = set(ingredients)

    return allergens


def part_1(foods):
    allergens = isolate_allergens(foods)

    allergen_free = set(i for ingredients, _ in foods for i in ingredients) - set.union(
        *allergens.values()
    )

    count = 0
    for ingredient in allergen_free:
        count += sum(ingredients.count(ingredient) for ingredients, _ in foods)

    return count


def part_2(foods):
    allergens = [
        v for k, v in sorted(isolate_allergens(foods).items(), key=lambda kv: kv[0])
    ]

    while any(len(a) > 1 for a in allergens):
        locked = [next(iter(a)) for a in allergens if len(a) == 1]
        for a in allergens:
            if len(a) == 1:
                continue
            else:
                for i in locked:
                    if i in a:
                        a.remove(i)

    return ",".join([next(iter(a)) for a in allergens])


if __name__ == "__main__":
    foods = load_data(sys.argv[1])
    print(f"Part 1: {part_1(foods)}")
    print(f"Part 2: {part_2(foods)}")
