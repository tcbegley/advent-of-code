import sys


def answer(file_path):
    with open(file_path, "r") as f:
        nums = list(map(int, f.read().strip()))
    return sum(
        [nums[i - 1] for i in range(len(nums)) if nums[i] == nums[i - 1]]
    )


if __name__ == "__main__":
    print(answer(sys.argv[1]))
