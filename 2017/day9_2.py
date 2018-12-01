import re
import sys


def answer(file_path):
    with open(file_path, 'r') as f:
        stream = f.read().strip()
    stream = re.sub(r'!.', '', stream)
    garbage = re.findall(r'<([^>]*)>', stream)
    return len(''.join(garbage))


if __name__ == "__main__":
    print(answer(sys.argv[1]))
