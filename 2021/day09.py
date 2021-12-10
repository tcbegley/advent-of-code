import sys


class UnionFind:
    def __init__(self, rows, cols):
        self.num_components = rows * cols
        self.id = {(r, c): (r, c) for r in range(rows) for c in range(cols)}
        self.size = {(r, c): 1 for r in range(rows) for c in range(cols)}

    def find(self, loc):
        root = loc
        while root != self.id[root]:
            root = self.id[root]

        # path compression
        while loc != root:
            next_ = self.id[loc]
            self.id[loc] = root
            loc = next_

        return root

    def component_size(self, loc):
        return self.size[self.find(loc)]

    def unify(self, loc1, loc2):
        root1 = self.find(loc1)
        root2 = self.find(loc2)

        if root1 != root2:
            if self.size[root1] < self.size[root2]:
                self.size[root2] += self.size[root1]
                self.id[root1] = root2
            else:
                self.size[root1] += self.size[root2]
                self.id[root2] = root1

            self.num_components += 1


def load_data(path):
    def process_line(line):
        return [int(i) for i in line.strip()]

    with open(path) as f:
        return [process_line(line) for line in f.readlines()]


def get_neighbours(row, col, caves):
    return [(row + i, col) for i in [-1, 1] if 0 <= row + i < len(caves)] + [
        (row, col + j) for j in [-1, 1] if 0 <= col + j < len(caves[0])
    ]


def is_low_point(row, col, caves):
    return all(
        caves[row][col] < caves[r][c]
        for r, c in get_neighbours(row, col, caves)
    )


def part_1(caves):
    return sum(
        1 + caves[i][j]
        for i in range(len(caves))
        for j in range(len(caves[0]))
        if is_low_point(i, j, caves)
    )


def part_2(caves):
    n_rows, n_cols = len(caves), len(caves[0])
    union_find = UnionFind(len(caves), len(caves[0]))

    for row in range(n_rows):
        for col in range(n_cols):
            if caves[row][col] == 9:
                continue
            for nbr in get_neighbours(row, col, caves):
                if caves[nbr[0]][nbr[1]] != 9:
                    union_find.unify((row, col), nbr)

    sizes = sorted(
        (
            union_find.component_size(loc)
            for loc in set(union_find.id.values())
        ),
        reverse=True,
    )
    return sizes[0] * sizes[1] * sizes[2]


if __name__ == "__main__":
    caves = load_data(sys.argv[1])
    print(f"Part 1: {part_1(caves)}")
    print(f"Part 2: {part_2(caves)}")
