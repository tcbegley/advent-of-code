import sys


class UnionFind:
    def __init__(self, x_range, y_range, z_range, grid):
        self.id = {
            (x, y, z): (x, y, z)
            for x in range(*x_range)
            for y in range(*y_range)
            for z in range(*z_range)
            if (x, y, z) not in grid
        }
        self.size = {
            (x, y, z): 1
            for x in range(*x_range)
            for y in range(*y_range)
            for z in range(*z_range)
            if (x, y, z) not in grid
        }
        self.num_components = len(self.id)

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

    def connected(self, loc1, loc2):
        return self.find(loc1) == self.find(loc2)

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


def load_data(path):
    with open(path) as f:
        return {
            tuple(map(int, row.split(",")))
            for row in f.read().strip().split("\n")
        }


def get_neighbours(droplet):
    x, y, z = droplet
    for dx, dy, dz in (
        (-1, 0, 0),
        (1, 0, 0),
        (0, -1, 0),
        (0, 1, 0),
        (0, 0, -1),
        (0, 0, 1),
    ):
        yield (x + dx, y + dy, z + dz)


def part_1(data):
    surface_area = 0
    for droplet in data:
        for nbr in get_neighbours(droplet):
            if nbr not in data:
                surface_area += 1

    return surface_area


def part_2(data):
    xs = {x for x, _, _ in data}
    ys = {y for _, y, _ in data}
    zs = {z for _, _, z in data}

    x_range = (min(xs) - 1, max(xs) + 2)
    y_range = (min(ys) - 1, max(ys) + 2)
    z_range = (min(zs) - 1, max(zs) + 2)

    components = UnionFind(x_range, y_range, z_range, data)

    for x in range(*x_range):
        for y in range(*y_range):
            for z in range(*z_range):
                if (x, y, z) in data:
                    continue
                for nbr in get_neighbours((x, y, z)):
                    if nbr in data or not (
                        x_range[0] <= nbr[0] < x_range[1]
                        and y_range[0] <= nbr[1] < y_range[1]
                        and z_range[0] <= nbr[2] < z_range[1]
                    ):
                        continue
                    components.unify((x, y, z), nbr)

    outside = (x_range[0], y_range[0], z_range[0])

    surface_area = 0
    for droplet in data:
        for nbr in get_neighbours(droplet):
            if nbr not in data and components.connected(nbr, outside):
                surface_area += 1

    return surface_area


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
