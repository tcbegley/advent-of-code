import re
import sys
from collections import defaultdict


def load_data(path):
    with open(path) as f:
        return [
            [
                [int(i) for i in x.split(",")]
                for x in re.findall(r"<([^>]*)>", particle)
            ]
            for particle in f.readlines()
        ]


def l1(x):
    return sum(map(abs, x))


class Particle:
    def __init__(self, p, v, a):
        self.p = p
        self.v = v
        self.a = a

    def update(self):
        self.v = [v + a for v, a in zip(self.v, self.a)]
        self.p = [p + v for p, v in zip(self.p, self.v)]

    def distance(self):
        return l1(self.p)


def part_1(particles):
    particles = [
        (i, Particle(*particle)) for i, particle in enumerate(particles)
    ]

    min_l1_a = min(l1(p.a) for _, p in particles)
    nearest = [(i, p) for i, p in particles if l1(p.a) == min_l1_a]

    min_l1_v = min(l1(p.v) for _, p in nearest)
    nearest = [(i, p) for i, p in nearest if l1(p.v) == min_l1_v]

    return nearest[0][0]


def part_2(particles):
    particles = dict(enumerate(Particle(*particle) for particle in particles))

    # no guarantee that 100 iterations is enough...
    for _ in range(100):
        for p in particles.values():
            p.update()

        positions = defaultdict(list)
        for i, p in particles.items():
            positions[tuple(p.p)].append(i)

        for particle_ids in positions.values():
            if len(particle_ids) > 1:
                for i in particle_ids:
                    particles.pop(i)

    return len(particles)


if __name__ == "__main__":
    particles = load_data(sys.argv[1])
    print(f"Part 1: {part_1(particles)}")
    print(f"Part 2: {part_2(particles)}")
