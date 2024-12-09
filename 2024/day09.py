import sys
from collections import deque
from dataclasses import dataclass, field


@dataclass
class File:
    id: int
    length: int
    moved: bool = False


@dataclass
class Gap:
    length: int
    files: list[File] = field(default_factory=list)


def load_data(path):
    with open(path) as f:
        return [int(n) for n in f.read().strip()]


def part_1(data):
    blocks = deque([i for i, n in enumerate(data[::2]) for _ in range(n)])

    checksum = 0
    idx = 0
    for i, n in enumerate(data):
        for _ in range(n):
            if not blocks:
                return checksum
            if i % 2 == 0:
                checksum += idx * blocks.popleft()
            else:
                checksum += idx * blocks.pop()
            idx += 1


def part_2(data):
    gaps = [Gap(length=length) for length in data[1::2]]
    files = [File(id=i, length=length) for i, length in enumerate(data[::2])]

    if len(gaps) < len(files):
        # add an empty cgp on the end just to make it easier to join up again later
        gaps.append(Gap(length=0))

    for file in reversed(files):
        for gap in gaps[: file.id]:
            if gap.length >= file.length:
                file.moved = True
                gap.length -= file.length
                gap.files.append(file)
                break

    checksum = idx = 0
    for file, gap in zip(files, gaps):
        if not file.moved:
            # if the file didn't move, add its contribution in place
            checksum += sum(file.id * i for i in range(idx, idx + file.length))
        idx += file.length

        for f in gap.files:
            # add contributions of all files we moved into the gap
            checksum += sum(f.id * i for i in range(idx, idx + f.length))
            idx += f.length
        idx += gap.length

    return checksum


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
