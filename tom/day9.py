import re
import sys


def parse(stream):
    parsed = []
    n = 0
    left = 1
    for i in range(len(stream)):
        if stream[i] == "{":
            n += 1
        if stream[i] == "}":
            n -= 1
        if n == 0:
            parsed.append(stream[left:i])
            left = i+2
    return parsed


def score(stream, n):
    return n + sum([score(x, n+1) for x in parse(stream)])


def answer(file_path):
    with open(file_path, 'r') as f:
        stream = f.read().strip()
    stream = re.sub(r'!.', '', stream)
    stream = re.sub(r'<[^>]*>', '', stream)
    stream = re.sub(r'[^{}]', '', stream)
    return score(stream, 0)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
