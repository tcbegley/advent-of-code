import sys


def answer(file_path):
    with open(file_path, "r") as f:
        pass_phrases = [x.strip().split(" ") for x in f.readlines()]
    return len([pp for pp in pass_phrases if len(pp) == len(set(pp))])


if __name__ == "__main__":
    print(answer(sys.argv[1]))
