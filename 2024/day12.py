import sys


class UnionFind:
    """
    UnionFind is a data structure for detemining connected components
    """

    def __init__(self, grid):
        self.num_components = len(grid)
        self.id = {k: k for k in grid}
        self.size = {k: 1 for k in grid}

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

            self.num_components -= 1

    def __iter__(self):
        components = {}
        for loc in self.id:
            components.setdefault(self.find(loc), set()).add(loc)

        return iter(components.values())


def load_data(path):
    with open(path) as f:
        grid = {
            c - r * 1j: char
            for r, row in enumerate(f.read().strip().split("\n"))
            for c, char in enumerate(row)
        }

    union_find = UnionFind(grid)

    for loc in grid:
        for d in (1, -1, 1j, -1j):
            if grid.get(nbr := loc + d) == grid[loc]:
                union_find.unify(loc, nbr)

    return union_find


def area(region):
    # area of a region is the number of locations in that region
    return len(region)


def perimeter(region):
    # each location in a region contributes to the perimeter the number of its
    # neighbours that are not also in the region
    return sum(sum(loc + d not in region for d in (-1, 1, -1j, 1j)) for loc in region)


def n_sides(region):
    checked = set()
    count = 0

    for loc in region:
        # for each location
        for d in (1, -1, 1j, -1j):
            # and each direction
            if (loc, d) in checked:
                # if we've been here before, continue
                continue
            checked.add((loc, d))

            # otherwise, if there is a side here
            if loc + d not in region:
                # add 1 to the count of sides
                count += 1
                # and move along the side in both directions, marking all other
                # locations that are part of the same side as having been visited
                nbr = loc + d * 1j
                while nbr in region and nbr + d not in region:
                    checked.add((nbr, d))
                    nbr += d * 1j
                nbr = loc - d * 1j
                while nbr in region and nbr + d not in region:
                    checked.add((nbr, d))
                    nbr -= d * 1j
    return count


def part_1(regions):
    return sum(area(component) * perimeter(component) for component in regions)


def part_2(regions):
    return sum(area(component) * n_sides(component) for component in regions)


if __name__ == "__main__":
    regions = load_data(sys.argv[1])
    print(f"Part 1: {part_1(regions)}")
    print(f"Part 2: {part_2(regions)}")
