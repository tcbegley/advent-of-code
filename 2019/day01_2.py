import sys


def get_fuel(mass):
    if mass <= 0:
        return 0
    fuel = max(mass // 3 - 2, 0)
    return fuel + get_fuel(fuel)


def answer(path):
    with open(path) as f:
        masses = [get_fuel(int(m)) for m in f.read().strip().split("\n")]
    return sum(masses)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
