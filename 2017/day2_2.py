import sys


def divide(row):
    for i in range(len(row)):
        for j in range(len(row)):
            if i == j:
                continue
            if row[i] % row[j] == 0:
                return row[i] // row[j]
    return None


def answer(file_path):
    with open(file_path, "r") as f:
        nums = [list(map(int, x.strip().split("\t"))) for x in f.readlines()]
    return sum([divide(row) for row in nums])


if __name__ == "__main__":
    print(answer(sys.argv[1]))
