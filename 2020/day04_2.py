import re
import sys


HCL_PATTERN = re.compile(r"^#[0-9a-z]{6}$")
PID_PATTERN = re.compile(r"^\d{9}$")


def valid(p):
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
