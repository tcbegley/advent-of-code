import re
import sys

ELEMENT = re.compile(r"[A-Z][a-z]*")


def load_data(path):
    with open(path) as f:
        replacements, molecule = f.read().strip().split("\n\n")

    replacements = [r.split(" => ") for r in replacements.split("\n")]
    return replacements, molecule


def step(replacements, molecule):
    possible = set()
    for original, replacement in replacements:
        start = 0
        len_original = len(original)
        while original in molecule[start:]:
            i = molecule.index(original, start)
            possible.add(
                "".join(
                    [molecule[:i], replacement, molecule[i + len_original :]]
                )
            )
            start = i + len_original
    return possible


def part_1(replacements, molecule):
    return len(step(replacements, molecule))


def part_2(replacements, molecule):
    elements = ELEMENT.findall(molecule)
    return (
        len(elements)
        - elements.count("Rn")
        - elements.count("Ar")
        - 2 * elements.count("Y")
        - 1
    )


if __name__ == "__main__":
    replacements, molecule = load_data(sys.argv[1])
    print(f"Part 1: {part_1(replacements, molecule)}")
    print(f"Part 2: {part_2(replacements, molecule)}")
