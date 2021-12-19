import sys
from collections import defaultdict, deque
from itertools import combinations, permutations


def load_data(path):
    def process_beacons(scanner):
        beacons = scanner.split("\n")[1:]
        return [tuple(int(i) for i in beacon.split(",")) for beacon in beacons]

    with open(path) as f:
        scanners = f.read().strip().split("\n\n")

    return [process_beacons(scanner) for scanner in scanners]


def l1(beacon1, beacon2):
    x1, y1, z1 = beacon1
    x2, y2, z2 = beacon2
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def get_distance_counts(beacons):
    distances = defaultdict(dict)
    for b1, b2 in permutations(beacons, 2):
        dist = l1(b1, b2)
        distances[b1][dist] = distances[b1].get(dist, 0) + 1
    return distances


def get_transform(pair1, pair2):
    diffs1 = tuple(a - b for a, b in zip(pair1[0], pair2[0]))
    diffs2 = tuple(a - b for a, b in zip(pair1[1], pair2[1]))

    permutation = {
        i: [abs(x) for x in diffs2].index(abs(value))
        for i, value in enumerate(diffs1)
    }
    reflect = [diffs1[i] != diffs2[permutation[i]] for i in range(3)]
    x, x_alt = pair1
    x_alt_transformed = tuple(
        -x_alt[permutation[i]] if reflect[i] else x_alt[permutation[i]]
        for i in range(3)
    )
    offset = tuple(x[i] - x_alt_transformed[i] for i in range(3))
    return permutation, reflect, offset


def get_transformed_locations(beacons1, beacons2):
    # check if there's overlap between two sets of beacons by comparing the
    # distances between different beacons (this is transformation independent)
    distances1 = get_distance_counts(beacons1)
    distances2 = get_distance_counts(beacons2)

    overlapping = []

    for b1, d1 in distances1.items():
        for b2, d2 in distances2.items():
            if sum(min(v, d2.get(k, 0)) for k, v in d1.items()) >= 11:
                overlapping.append((b1, b2))
                break

    # we are told that if there is any overlap, then at least 12 beacons are
    # shared between two sets
    if len(overlapping) < 12:
        return [], None

    # if we have found overlap then we can figure out how to transform back
    # to the base coordinates and return the transformed coordinates.
    permutation, reflect, offset = get_transform(
        overlapping[0], overlapping[1]
    )
    beacons2 = [
        tuple(
            -b[permutation[i]] + offset[i]
            if reflect[i]
            else b[permutation[i]] + offset[i]
            for i in range(3)
        )
        for b in beacons2
    ]

    return beacons2, offset


def locate(beacons):
    unique_beacons = set(beacons[0])
    queue = deque(beacons[1:])
    scanners = [(0, 0, 0)]

    while queue:
        # get a set of beacons
        beacons_other = queue.popleft()
        # see if there's any overlap and get the transformed locations + the
        # offset, which is the same as the scanner location
        transformed_locations, offset = get_transformed_locations(
            unique_beacons, beacons_other
        )
        if transformed_locations:
            unique_beacons.update(transformed_locations)
            scanners.append(offset)
        else:
            queue.append(beacons_other)

    return unique_beacons, scanners


def part_1(unique_beacons):
    return len(unique_beacons)


def part_2(scanners):
    return max(
        l1(scanner1, scanner2)
        for scanner1, scanner2 in combinations(scanners, 2)
    )


if __name__ == "__main__":
    beacons = load_data(sys.argv[1])
    unique_beacons, scanners = locate(beacons)
    print(f"Part 1: {part_1(unique_beacons)}")
    print(f"Part 2: {part_2(scanners)}")
