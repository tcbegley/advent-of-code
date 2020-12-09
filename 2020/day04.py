import re
import sys

FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

HCL_PATTERN = re.compile(r"^#[0-9a-z]{6}$")
PID_PATTERN = re.compile(r"^\d{9}$")


def load_data(path):
    with open(path) as f:
        passports = f.read().strip().replace("\n", " ").split("  ")

    return [
        dict([x.split(":") for x in passport.split(" ")])
        for passport in passports
    ]


def valid_1(p):
    for field in FIELDS:
        if field not in p:
            return False
    return True


def valid_2(p):
    try:
        if not (len(p["byr"]) == 4 and 1920 <= int(p["byr"]) <= 2002):
            return False
        if not (len(p["iyr"]) == 4 and 2010 <= int(p["iyr"]) <= 2020):
            return False
        if not (len(p["eyr"]) == 4 and 2020 <= int(p["eyr"]) <= 2030):
            return False
        if p["hgt"][-2:] == "cm":
            if not (150 <= int(p["hgt"][:-2]) <= 193):
                return False
        elif p["hgt"][-2:] == "in":
            if not (59 <= int(p["hgt"][:-2]) <= 76):
                return False
        else:
            return False
        if not HCL_PATTERN.match(p["hcl"]):
            return False
        if p["ecl"] not in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}:
            return False
        if not PID_PATTERN.match(p["pid"]):
            return False
    except KeyError:
        return False
    return True


def count_valid(valid, passports):
    return sum(map(valid, passports))


if __name__ == "__main__":
    passports = load_data(sys.argv[1])
    print(f"Part 1: {count_valid(valid_1, passports)}")
    print(f"Part 2: {count_valid(valid_2, passports)}")
