import heapq
import re
import sys
from itertools import chain, combinations, product

GENERATOR_PATTERN = re.compile(r"(\w+) generator")
MICROCHIP_PATTERN = re.compile(r"(\w+)-compatible microchip")


def load_data(path):
    with open(path) as f:
        lines = f.readlines()

    generators = [GENERATOR_PATTERN.findall(line) for line in lines]
    microchips = [MICROCHIP_PATTERN.findall(line) for line in lines]

    elements = {el: i for i, el in enumerate(set(chain(*generators)), start=1)}

    return normalise_floors(
        {elements[g] for g in gen} | {-elements[m] for m in mic}
        for gen, mic in zip(generators, microchips)
    )


def normalise_floors(floors):
    floors = tuple(tuple(sorted(floor)) for floor in floors)
    # we remap the enumeration of the items on each floor so that the search
    # space doesn't explode due to symmetry
    mapping = {
        j: i
        for i, j in enumerate(
            chain(*[(x for x in floor if x > 0) for floor in floors]), start=1
        )
    }
    return tuple(
        tuple(mapping[x] if x > 0 else -mapping[-x] for x in floor)
        for floor in floors
    )


def get_lower_bound(floors, loc):
    """
    Computes a lower bound for the number of moves required to move all chips
    and generators to the top.

    The optimal strategy is to move to the bottom layer (taking one item to
    power the elevator), then move all items up to the next floor (move two
    items up then one item down until two remain then move both up together).

    This process repeats until everything is on the top floor. This lower bound
    doesn't take into account other compatibility conditions such as valid
    combinations of items in elevators / on floors.
    """

    def add_min_moves(count):
        # number of moves required to move `count` items up to the next floor
        if count <= 2:
            # if 2 items or fewer, can do it in a single move
            return 1
        # otherwise we require two moves per item (take two up, move one back
        # down) except the last two which require only one move
        return 2 * (count - 2) + 1

    # initialise lower bound
    lower_bound = 0

    # count the number of items on each floor
    counts = [len(floor) for floor in floors]

    # find out which is the lowest floor with items
    first_non_empty = [count > 0 for count in counts].index(True)

    if loc < first_non_empty:
        # if we start below the first floor with items, we don't have anything
        # to power the elevator!
        raise ValueError(
            "You need an item on the current floor to power the elevator"
        )
    elif loc > first_non_empty:
        # we move down to the lowest non-empty floor, taking one item with us
        lower_bound += loc - first_non_empty
        counts[loc] -= 1
        counts[first_non_empty] += 1

    cumulative_count = 0
    for count in counts[:-1]:
        # for each floor except the last, we move all items to the next floor
        cumulative_count += count
        lower_bound += add_min_moves(cumulative_count)

    return lower_bound


def items_are_valid(items):
    # items are only invalid if there is a non-matching chip and generator
    # so ok if there is only one item, if both items have same sign or if both
    # items have the same magnitude (i.e. type)
    return (
        len(items) == 1
        or items[0] * items[1] > 0
        or abs(items[0]) == abs(items[1])
    )


def floor_is_valid(floor):
    if not floor or floor[-1] < 0:
        # floor is empty or only microchips are on this floor
        return True
    # if there is even a single generator, then all microchips must have their
    # corresponding generators present otherwise they get fried
    return all(-chip in floor for chip in floor if chip < 0)


def end_state(floors, loc):
    # we're on the top floor and all lower floors are empty
    return loc == len(floors) - 1 and all(len(f) == 0 for f in floors[:-1])


def move_items(floors, loc, items, direction):
    # move items from floor at loc to floor at loc + direction
    return normalise_floors(
        floor + items
        if i == loc + direction
        else ((x for x in floor if x not in items) if i == loc else floor)
        for i, floor in enumerate(floors)
    )


def count_steps(floors):
    steps_taken = {(0, floors): 0}

    queue = []
    heapq.heappush(queue, (get_lower_bound(floors, 0), 0, floors))

    while queue:
        _, loc, floors = heapq.heappop(queue)
        steps = steps_taken[(loc, floors)]
        if end_state(floors, loc):
            return steps

        for direction, items in product(
            [d for d in (-1, 1) if 0 <= loc + d < len(floors)],
            chain(combinations(floors[loc], 2), combinations(floors[loc], 1)),
        ):
            if not items_are_valid(items):
                continue

            new_floors = move_items(floors, loc, items, direction)
            if not all(map(floor_is_valid, new_floors)):
                continue

            key = (loc + direction, new_floors)
            if key not in steps_taken or steps_taken[key] > steps + 1:
                steps_taken[key] = steps + 1
                lower_bound = get_lower_bound(new_floors, loc + direction)
                heapq.heappush(queue, (steps + 1 + lower_bound,) + key)


def part_1(floors):
    return count_steps(floors)


def part_2(floors):
    n = max(max(floor, default=0) for floor in floors)
    floors = (
        (-n - 2, -n - 1) + floors[0] + (n + 1, n + 2),
        floors[1],
        floors[2],
        floors[3],
    )
    return count_steps(floors)


if __name__ == "__main__":
    floors = load_data(sys.argv[1])
    print(f"Part 1: {part_1(floors)}")
    print(f"Part 2: {part_2(floors)}")
