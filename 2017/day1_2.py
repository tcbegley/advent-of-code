import sys


def answer(file_path):
    with open(file_path, "r") as f:
        nums = list(map(int, f.read().strip()))
    n = len(nums)
    return sum(
        [
            nums[i]
            for i in range(len(nums))
            if nums[i] == nums[(i + n // 2) % n]
        ]
    )


if __name__ == "__main__":
    print(answer(sys.argv[1]))
