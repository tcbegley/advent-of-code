import sys
from dataclasses import dataclass
from itertools import combinations

import numpy as np


@dataclass
class Hailstone:
    position: tuple[int, int, int]
    velocity: tuple[int, int, int]

    def position_at_time(self, t):
        return tuple(self.position[i] + t * self.velocity[i] for i in range(3))

    def time_at_coord_position(self, position, coord):
        return (position - self.position[coord]) / self.velocity[coord]

    @property
    def cm(self):
        m = self.velocity[1] / self.velocity[0]
        return (self.position[1] - self.position[0] * m, m)

    def will_collide(
        self,
        other: "Hailstone",
        coord_min=200_000_000_000_000,
        coord_max=400_000_000_000_000,
    ):
        c_self, m_self = self.cm
        c_other, m_other = other.cm

        if m_self == m_other:
            return False

        x = (c_other - c_self) / (m_self - m_other)
        y = m_self * x + c_self
        return (
            self.time_at_coord_position(x, 0) >= 0
            and other.time_at_coord_position(x, 0) >= 0
            and self.time_at_coord_position(y, 1) >= 0
            and other.time_at_coord_position(y, 1) >= 0
            and coord_min <= x <= coord_max
            and coord_min <= y <= coord_max
        )


def process_row(row):
    position, velocity = row.split(" @ ")
    return Hailstone(
        tuple(map(int, position.split(", "))), tuple(map(int, velocity.split(", ")))
    )


def load_data(path):
    with open(path) as f:
        return [process_row(row) for row in f.read().strip().split("\n")]


def part_1(data):
    return sum(hs1.will_collide(hs2) for hs1, hs2 in combinations(data, 2))


def part_2(data):
    # let p, v be the initial position and velocity of the rock we want ot throw
    # let pi, vi be the initial position and velocity of hailstone i.
    # then we require that for each i there is a ti such that p + ti * v = pi + ti * vi
    # or in other words (p - pi) + ti * (v - vi) = 0
    # thus (p - pi) x (v - vi) = 0 since they are colinear.
    # this equation is not linear in the unknowns p and v, however the quadratic terms
    # are the same for each i, so we can cancel and instead solve
    # v x (p2 - p1) + p x (v2 - v1) = p2 x v2 - p1 x v1
    # v x (p3 - p1) + p x (v3 - v1) = p3 x v3 - p1 x v1
    # TODO: solve this using only standard library??
    p1 = np.array(data[0].position)
    p2 = np.array(data[1].position)
    p3 = np.array(data[2].position)
    v1 = np.array(data[0].velocity)
    v2 = np.array(data[1].velocity)
    v3 = np.array(data[2].velocity)

    A1 = np.concatenate(
        [np.cross((v2 - v1), np.eye(3)), np.cross((p2 - p1), np.eye(3))], axis=1
    )
    A2 = np.concatenate(
        [np.cross((v3 - v1), np.eye(3)), np.cross((p3 - p1), np.eye(3))], axis=1
    )
    A = np.concatenate([A1, A2])
    b = np.concatenate(
        [np.cross(p2, v2) - np.cross(p1, v1), np.cross(p3, v3) - np.cross(p1, v1)]
    )
    return np.linalg.solve(A, b)[:3].round().astype(np.int64).sum()


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
