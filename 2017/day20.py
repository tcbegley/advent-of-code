import re
import sys


class Particle:
    def __init__(self, p, v, a):
        self.p = p
        self.v = v
        self.a = a

    def update(self):
        self.p = [p + v for p, v in zip(self.p, self.v)]
        self.v = [v + a for v, a in zip(self.v, self.a)]

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
    particles = [Particle(*particle) for particle in particles]
    while True:
        for particle in particles:
            particle.update()
        min_dist, min_loc = float("inf"), None
        for i, particle in enumerate(particles):
            dist = particle.distance()
            if dist < min_dist:
                min_dist, min_loc = dist, i
        print(min_loc)


if __name__ == "__main__":
    print(answer(sys.argv[1]))
