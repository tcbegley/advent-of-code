import heapq
import re
import sys
from copy import copy
from itertools import product

# Coordinate system

#      012345678910
#     #############
#   0 #...........#
#   1 ###.#.#.#.###
#   2   #.#.#.#.#
#   3   #.#.#.#.#
#   4   #.#.#.#.#
#   5   #########

LETTER = re.compile(r"[A-D]")
ROOM_XS = {2: "A", 4: "B", 6: "C", 8: "D"}
SCORE = {"A": 1, "B": 10, "C": 100, "D": 1000}


def load_data(path):
    with open(path) as f:
        letters = LETTER.findall(f.read())

    locs = [(2, 1), (4, 1), (6, 1), (8, 1), (2, 2), (4, 2), (6, 2), (8, 2)]
    return dict(zip(locs, letters))


def scan_corridor(x_range, amphipod, amphipods, neighbours, room_size):
    (_, y), amphipod_type = amphipod

    for i in x_range:
        if (i, 0) in amphipods:
            # this spot is occupied, we can't get past!
            break

        if i in ROOM_XS:
            # can't stop in front of room, but can maybe go inside
            if amphipod_type == ROOM_XS[i]:
                first_occupied = min(
                    (
                        j
                        for j in range(1, room_size + 1)
                        if (i, j) in amphipods
                    ),
                    default=None,
                )
                if first_occupied is None:
                    # if room is empty, move to last slot
                    neighbours.append((i, room_size))
                elif all(
                    amphipods[(i, j)] == ROOM_XS[i]
                    for j in range(first_occupied, room_size + 1)
                ):
                    # if room is already occupied, only enter if all other
                    # occupants are in the right place
                    neighbours.append((i, first_occupied - 1))
        elif y > 0:
            # can only stop in the corridor if we just came out of a room
            neighbours.append((i, 0))


def get_neighbours(amphipod, amphipods, room_size):
    neighbours = []
    (x, y), amphipod_type = amphipod
    if y > 0:
        # we're in a room
        if any((x, i) in amphipods for i in range(y - 1, 0, -1)) or all(
            amphipods[(x, i)] == ROOM_XS[x] for i in range(y, room_size + 1)
        ):
            # either we're blocked in or we're in the right place and
            # everything below us is too, so don't move anywhere
            return []

    # scan corridor in both directions for possible end locations
    scan_corridor(range(x + 1, 11), amphipod, amphipods, neighbours, room_size)
    scan_corridor(
        range(x - 1, -1, -1), amphipod, amphipods, neighbours, room_size
    )

    return neighbours


def normalise(amphipods):
    return tuple(sorted(amphipods.items()))


def end_state(amphipods, room_size):
    target = normalise(
        {(x, y + 1): t for x, t in ROOM_XS.items() for y in range(room_size)}
    )
    return normalise(amphipods) == target


def lower_bound(amphipods, room_size):
    # crude lower bound on score required to get to right answer
    target_x = {v: k for k, v in ROOM_XS.items()}
    score = 0
    for loc, amphipod_type in amphipods.items():
        steps = 0
        target = target_x[amphipod_type]
        if target != loc[0]:
            steps += abs(target - loc[0]) + 2
        elif any(
            amphipods[(loc[0], i)] != amphipod_type
            for i in range(loc[1] + 1, room_size + 1)
        ):
            # have to move out of the way and then back to let other amphipod
            # out of the room
            steps = 4
        score += steps * SCORE[amphipod_type]
    return score


def bfs(amphipods, room_size=2):
    queue = []
    heapq.heappush(queue, (0, normalise(amphipods)))
    visited = {normalise(amphipods): 0}

    while queue:
        _, amphipods = heapq.heappop(queue)
        score = visited[amphipods]
        amphipods = dict(amphipods)

        if end_state(amphipods, room_size=room_size):
            return score

        for loc, amphipod_type in amphipods.items():
            for nbr in get_neighbours(
                (loc, amphipod_type), amphipods, room_size=room_size
            ):
                new_amphipods = copy(amphipods)
                del new_amphipods[loc]
                new_amphipods[nbr] = amphipod_type
                new_score = (
                    score
                    + (loc[1] + nbr[1] + abs(loc[0] - nbr[0]))
                    * SCORE[amphipod_type]
                )
                normalised_amphipods = normalise(new_amphipods)
                if (
                    normalised_amphipods not in visited
                    or visited[normalised_amphipods] > new_score
                ):
                    visited[normalised_amphipods] = new_score
                    priority = new_score + lower_bound(
                        new_amphipods, room_size=room_size
                    )
                    heapq.heappush(queue, (priority, normalised_amphipods))

    return -1  # no solution found


def part_1(amphipods):
    return bfs(amphipods)


def part_2(amphipods):
    amphipods = {
        (x, y if y == 1 else 4): amphipod_type
        for (x, y), amphipod_type in amphipods.items()
    }
    new_locs = product([2, 4, 6, 8], [2, 3])
    new_types = ["D", "D", "C", "B", "B", "A", "A", "C"]

    for loc, amphipod_type in zip(new_locs, new_types):
        amphipods[loc] = amphipod_type

    return bfs(amphipods, room_size=4)


if __name__ == "__main__":
    amphipods = load_data(sys.argv[1])
    print(f"Part 1: {part_1(amphipods)}")
    print(f"Part 2: {part_2(amphipods)}")
