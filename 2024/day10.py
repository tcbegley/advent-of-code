import sys
from collections import deque


def load_data(path):
    with open(path) as f:
        return {
            c - r * 1j: int(char)
            for r, row in enumerate(f.read().strip().split("\n"))
            for c, char in enumerate(row)
        }


def get_score(trailhead, grid):
    queue = deque([trailhead])
    seen = set()
    score = 0

    while queue:
        loc = queue.popleft()
        if grid[loc] == 9:
            score += 1
        else:
            for d in (-1, 1, -1j, 1j):
                if (
                    (new_loc := loc + d) not in seen
                    and new_loc in grid
                    and grid[new_loc] == grid[loc] + 1
                ):
                    queue.append(new_loc)
                    seen.add(new_loc)

    return score


def get_rating(trailhead, grid):
    rating = 0

    def backtrack(loc):
        if grid[loc] == 9:
            nonlocal rating
            rating += 1
        else:
            for d in (-1, 1, -1j, 1j):
                if (new_loc := loc + d) in grid and grid[new_loc] == grid[loc] + 1:
                    backtrack(new_loc)

    backtrack(trailhead)
    return rating


def part_1(grid):
    return sum(
        get_score(trailhead, grid) for trailhead, height in grid.items() if height == 0
    )


def part_2(grid):
    return sum(
        get_rating(trailhead, grid) for trailhead, height in grid.items() if height == 0
    )


if __name__ == "__main__":
    grid = load_data(sys.argv[1])
    print(f"Part 1: {part_1(grid)}")
    print(f"Part 2: {part_2(grid)}")
