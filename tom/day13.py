import sys
from collections import defaultdict


def answer(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().strip().split('\n')
    lines = [list(map(int, line.split(': '))) for line in lines]
    for line in lines:
        line[1] = line[1] * 2 - 2
    layers = defaultdict(lambda: 0)
    for line in lines:
        layers[line[0]] = line[1]
    severity = 0
    for i in range(max(layers.keys()) + 1):
        if layers[i] and i % layers[i] == 0:
            severity += i * (layers[i] + 2) // 2
    return severity


if __name__ == "__main__":
    print(answer(sys.argv[1]))
