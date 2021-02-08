import re
import sys
from collections import Counter, deque
from string import ascii_lowercase

ROOM = re.compile(r"([a-z-]+)-(\d+)\[([a-z]+)\]")


def load_data(path):
    with open(path) as f:
        rooms = [ROOM.fullmatch(line) for line in f.read().strip().split("\n")]
    return [
        (room.group(1), int(room.group(2)), room.group(3)) for room in rooms
    ]


def valid_room(room):
    most_common = sorted(
        Counter(room[0].replace("-", "")).most_common(),
        key=lambda x: x[0],
    )
    most_common = sorted(
        most_common,
        key=lambda x: x[1],
        reverse=True,
    )
    return "".join(x[0] for x in most_common).startswith(room[2])


def decrypt(name, n):
    target = deque(ascii_lowercase)
    target.rotate(-n % 26)
    lookup = dict(zip(ascii_lowercase, target))
    lookup["-"] = " "

    return "".join(lookup[c] for c in name)


def part_1(rooms):
    return sum(room[1] for room in rooms if valid_room(room))


def part_2(rooms):
    for room in filter(valid_room, rooms):
        name = decrypt(room[0], room[1])

        if name == "northpole object storage":
            break

    return room[1]


if __name__ == "__main__":
    rooms = load_data(sys.argv[1])
    print(f"Part 1: {part_1(rooms)}")
    print(f"Part 2: {part_2(rooms)}")
