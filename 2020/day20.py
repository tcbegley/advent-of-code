import re
import sys
from collections import Counter

ID_PATTERN = re.compile(r"Tile (\d+):")

MONSTER_MASK = [
    (0, 18),
    (1, 0),
    (1, 5),
    (1, 6),
    (1, 11),
    (1, 12),
    (1, 17),
    (1, 18),
    (1, 19),
    (2, 1),
    (2, 4),
    (2, 7),
    (2, 10),
    (2, 13),
    (2, 16),
]


class Tile:
    def __init__(self, id_, body, edges):
        self.id_ = id_
        self.body = body
        self.edges = edges

    def __repr__(self):
        return f"<Tile id={self.id_}>"

    def reflect_v(self):
        return Tile(
            self.id_,
            [row[::-1] for row in self.body],
            [self.edges[i][::-1] for i in [0, 3, 2, 1]],
        )

    def reflect_h(self):
        return Tile(
            self.id_,
            [row for row in reversed(self.body)],
            [self.edges[i][::-1] for i in [2, 1, 0, 3]],
        )

    def _rotate(self):
        n = len(self.body)
        body = [
            "".join(self.body[-(j + 1)][i] for j in range(n)) for i in range(n)
        ]
        edges = [self.edges[i] for i in [3, 0, 1, 2]]
        return Tile(self.id_, body, edges)

    def rotate(self, quarter_turns):
        tile = Tile(self.id_, self.body, self.edges)
        for _ in range(quarter_turns):
            tile = tile._rotate()
        return tile


def load_data(path):
    with open(path) as f:
        return [process_tile(tile) for tile in f.read().strip().split("\n\n")]


def process_tile(tile):
    id_line, *tile = tile.split("\n")

    id_ = int(ID_PATTERN.match(id_line).group(1))
    body = [row[1:-1] for row in tile[1:-1]]
    edges = [
        tile[0],
        "".join(row[-1] for row in tile),
        tile[-1][::-1],
        "".join(row[0] for row in reversed(tile)),
    ]

    return Tile(id_, body, edges)


def count_edges(tiles):
    edges = [e for t in tiles for e in t.edges]
    edges += [e[::-1] for e in edges]
    return Counter(edges)


def find_match(target, tiles, orient=0):
    """
    `orient` specifies orientation of target edge

        0
        |
    3 - t - 1
        |
        2

    If matching to 0, edge needs to be in location 2, 1 -> 3, 2 -> 0, 3 -> 1.
    """
    tile_lookup = {}
    for tile in tiles:
        for edge in tile.edges:
            tile_lookup.setdefault(edge, []).append(tile)
            tile_lookup.setdefault(edge[::-1], []).append(tile)

    if target not in tile_lookup:
        raise ValueError("No match")

    tile = tile_lookup[target][0]

    if target[::-1] not in tile.edges:
        tile = tile.reflect_h()

    idx = tile.edges.index(target[::-1])
    target_idx = (orient + 2) % 4

    if idx != target_idx:
        tile = tile.rotate((target_idx - idx) % 4)

    return tile


def get_neighbours(loc):
    for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
        yield (loc[0] + dx, loc[1] + dy)


def assemble_tiles(tiles):
    image = {(0, 0): tiles[0]}
    visited = set()
    tiles = tiles[1:]

    while (to_visit := set(image.keys()) - visited) :
        for loc in to_visit:
            visited.add(loc)

            tile = image[loc]
            for orient, nbr in enumerate(get_neighbours(loc)):
                if nbr in image:
                    continue

                try:
                    match = find_match(tile.edges[orient], tiles, orient)
                except ValueError:
                    continue

                image[nbr] = match
                tiles = [t for t in tiles if t.id_ != match.id_]

    x = [x for x, _ in image.keys()]
    y = [y for _, y in image.keys()]
    min_x, max_x = min(x), max(x)
    min_y, max_y = min(y), max(y)

    return [
        [image[(i, j)].body for j in range(min_y, max_y + 1)]
        for i in range(min_x, max_x + 1)
    ]


def monster_hunt(body):
    count = 0
    for x in range(len(body) - 2):
        for y in range(len(body[0]) - 19):
            if all(body[x + dx][y + dy] == "#" for dx, dy in MONSTER_MASK):
                count += 1

    return count


def check_rotations(image):
    for _ in range(4):
        count = monster_hunt(image.body)
        if count > 0:
            return count
        image = image.rotate(1)
    return 0


def part_1(tiles):
    # if we can find four tiles that have two edges that don't appear elsewhere
    # in the set of tiles, those have to be the four corners
    edge_counts = count_edges(tiles)
    result = 1
    for t in tiles:
        count = 0
        # only need to check one of the edges
        for edge in t.edges:
            if edge_counts[edge] >= 2:
                count += 1
        if count <= 2:
            result *= t.id_

    return result


def part_2(tiles):
    image = assemble_tiles(tiles)
    # abuse Tile class for rotation / reflection purposes
    image = Tile(
        None,
        "\n".join(
            "\n".join("".join(x) for x in zip(*row)) for row in image
        ).split("\n"),
        ["a", "a", "a", "a"],
    )

    count = check_rotations(image) or check_rotations(image.reflect_v())
    return "".join(image.body).count("#") - count * 15


if __name__ == "__main__":
    tiles = load_data(sys.argv[1])
    print(f"Part 1: {part_1(tiles)}")
    print(f"Part 2: {part_2(tiles)}")
