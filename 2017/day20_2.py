import re
import sys
from collections import defaultdict
import time


class Particle:
    def __init__(self, p, v, a):
        self.p = p
        self.v = v
        self.a = a

    def update(self):
        self.v = [v + a for v, a in zip(self.v, self.a)]
        self.p = [p + v for p, v in zip(self.p, self.v)]

    def distance(self):
        return sum(abs(c) for c in self.p)


def answer(file_path):
    with open(file_path, "r") as f:
        particles = f.readlines()
    particles = [
        [
            list(map(int, x.split(",")))
            for x in re.findall(r"<([^>]*)>", particle)
        ]
        for particle in particles
    ]
    particles = dict(enumerate(Particle(*particle) for particle in particles))
    while True:
        for p in particles.values():
            p.update()
        positions = defaultdict(list)
        for i, p in particles.items():
            positions[tuple(p.p)].append(i)
        for l in positions.values():
            if len(l) > 1:
                for i in l:
                    particles.pop(i)
        print(len(particles))


if __name__ == "__main__":
    print(answer(sys.argv[1]))
