import sys


class Ship:
    VECTORS = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}
    DIRECTIONS = ["N", "E", "S", "W"]
    ROTATION = [
        [[0, 1], [1, 1]],
        [[1, 1], [0, -1]],
        [[0, -1], [1, -1]],
        [[1, -1], [0, 1]],
    ]

    def __init__(self):
        self.x = 0
        self.y = 0
        self.dir = "E"
        self.w = [10, 1]

    def rotate_waypoint(self, action, value):
        if action == "L":
            # convert left rotation to right rotation
            value = 360 - value

        rotx, roty = self.ROTATION[value // 90]
        self.w = [self.w[rotx[0]] * rotx[1], self.w[roty[0]] * roty[1]]

    def navigate(self, instructions):
        for action, value in instructions:
            if action in self.VECTORS:
                x, y = self.VECTORS[action]
                self.x += x * value
                self.y += y * value
            elif action == "F":
                x, y = self.VECTORS[self.dir]
                self.x += x * value
                self.y += y * value
            elif action == "R":
                self.dir = self.DIRECTIONS[
                    (self.DIRECTIONS.index(self.dir) + value // 90) % 4
                ]
            elif action == "L":
                self.dir = self.DIRECTIONS[
                    (self.DIRECTIONS.index(self.dir) - value // 90) % 4
                ]

    def waypoint_navigate(self, instructions):
        for action, value in instructions:
            if action == "L" or action == "R":
                self.rotate_waypoint(action, value)
            elif action in self.VECTORS:
                x, y = self.VECTORS[action]
                self.w = [self.w[0] + x * value, self.w[1] + y * value]
            elif action == "F":
                self.x += self.w[0] * value
                self.y += self.w[1] * value


def load_data(path):
    with open(path) as f:
        return [(x[0], int(x[1:])) for x in f.read().strip().split("\n")]


def part_1(directions):
    s = Ship()
    s.navigate(directions)
    return abs(s.x) + abs(s.y)


def part_2(directions):
    s = Ship()
    s.waypoint_navigate(directions)
    return abs(s.x) + abs(s.y)


if __name__ == "__main__":
    instructions = load_data(sys.argv[1])
    print(f"Part 1: {part_1(instructions)}")
    print(f"Part 2: {part_2(instructions)}")
