import sys


def no_anagrams(pp):
    pp = list(map(sorted, map(list, pp)))
    return not any(pp.count(x) > 1 for x in pp)


def answer(file_path):
    with open(file_path, 'r') as f:
        pass_phrases = [x.strip().split(' ') for x in f.readlines()]
    return len([pp for pp in pass_phrases if no_anagrams(pp)])


if __name__ == "__main__":
    print(answer(sys.argv[1]))
