import sys

FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]


def valid(passport):
    for field in FIELDS[:-1]:
        if field not in passport:
            return False
    return True


def answer(path):
    with open(path) as f:
        passports = f.read().strip().replace("\n", " ").split("  ")

    passports = [
        dict([x.split(":") for x in passport.split(" ")])
        for passport in passports
    ]

    return sum(valid(p) for p in passports)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
