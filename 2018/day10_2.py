import re
import sys


class Particle:
    def __init__(self, px, py, vx, vy):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy

    def pos(self, time):
        return (self.px + time * self.vx, self.py + time * self.vy)


def answer(path):
    with open(path) as f:
        data = f.read().strip().split("\n")

    particles = []
    pattern = re.compile(r"<([^<>]*)>")
    for line in data:
        m = pattern.findall(line)
        px, py = [int(i) for i in m[0].split(",")]
        vx, vy = [int(i) for i in m[1].split(",")]
        particles.append(Particle(px, py, vx, vy))

    minw = float("inf")
    to_print = None
    increasing = 0
    i = 0

    while True:
        i += 1
        pos = [p.pos(i) for p in particles]
        minx = min(p[0] for p in pos)
        maxx = max(p[0] for p in pos)

        if maxx - minx < minw:
            minw = maxx - minx
            to_print = i
            increasing = 0
        else:
            increasing += 1

        if increasing > 10:
            break

    return to_print


if __name__ == "__main__":
    print(answer(sys.argv[1]))
