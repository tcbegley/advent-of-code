import re
import sys
from dataclasses import dataclass

NUMBER = re.compile(r"-?\d+")


@dataclass
class Particle:
    position: tuple[int, int]
    velocity: tuple[int, int]

    def pos(self, t):
        x, y = self.position
        vx, vy = self.velocity
        return (x + t * vx, y + t * vy)


def load_data(path):
    with open(path) as f:
        data = [map(int, NUMBER.findall(row)) for row in f.read().strip().split("\n")]
    return [Particle((x, y), (vx, vy)) for x, y, vx, vy in data]


def visualise(particles, t):
    particle_lookup = {p.pos(t) for p in particles}
    xs = [x for x, _ in particle_lookup]
    ys = [y for _, y in particle_lookup]

    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    return "\n" + "\n".join(
        "".join(
            "#" if (x, y) in particle_lookup else "." for x in range(minx, maxx + 1)
        )
        for y in range(miny, maxy + 1)
    )


def binary_search(f, low, high):
    # find the minimum of a convex function on the integers. we use a simple
    # finite difference to check if function is increasing or decreasing at
    # the midpoint. If it is decreasing before and non-decreasing after then
    # the midpoint is the minimum
    mid = low + (high - low) // 2
    f1, f2, f3 = f(mid - 1), f(mid), f(mid + 1)
    if f1 > f2:
        if f2 <= f3:
            return mid
        return binary_search(f, mid, high)
    return binary_search(f, low, mid)


def solve(particles):
    # since particles all have constant velocity, the minimum width of the
    # particle cluster will be convex, hence we can find the time at which
    # width is minimised with a binary search
    def f(t):
        xs = [p.pos(t)[0] for p in particles]
        return max(xs) - min(xs)

    # can conservatively assume that message appears in the first 1M steps
    t = binary_search(f, 0, 1_000_000)
    return visualise(particles, t), t


if __name__ == "__main__":
    particles = load_data(sys.argv[1])
    message, t = solve(particles)
    print(f"Part 1: {message}")
    print(f"Part 2: {t}")
