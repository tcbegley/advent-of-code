import sys


def answer(file_path):
    with open(file_path, "r") as f:
        nums = [list(map(int, x.strip().split("\t"))) for x in f.readlines()]
    return sum([max(row) - min(row) for row in nums])


if __name__ == "__main__":
    print(answer(sys.argv[1]))
