import sys
from collections import deque


def process_row(row):
    lights, *buttons, joltage = row.split(" ")
    lights = tuple(c == "#" for c in lights.strip("[]"))
    buttons = sorted(
        (tuple(map(int, button.strip("()").split(","))) for button in buttons),
        key=len,
        reverse=True,
    )
    joltage = tuple(map(int, joltage.strip(r"{}").split(",")))
    return lights, buttons, joltage


def load_data(path):
    with open(path) as f:
        return [process_row(row) for row in f.read().strip().split("\n")]


def bfs(lights, buttons):
    state = tuple(False for _ in lights)
    seen = {state}
    queue = deque([(0, state)])

    while queue:
        presses, state = queue.popleft()

        if state == lights:
            return presses

        for button in buttons:
            new_state = tuple(
                not light if i in button else light for i, light in enumerate(state)
            )
            if new_state not in seen:
                queue.append((presses + 1, new_state))
                seen.add(new_state)


def part_1(data):
    return sum(bfs(lights, buttons) for lights, buttons, _ in data)


def part_2(data):
    _, buttons, joltage = data
    n_buttons = len(buttons)
    n_lights = len(joltage)

    A = [[0] * n_buttons for _ in range(n_lights)]
    # we want to find x such that A @ x = joltage. obviously we would ideally import
    # some linear programming library here, but the rules i've set myself are standard
    # library only... so here we go!

    # A will not have full rank in general, so we need to compute row echelon form
    return data


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
