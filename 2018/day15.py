import sys
from collections import deque
from copy import deepcopy
from dataclasses import dataclass


@dataclass
class Player:
    loc: tuple[int, int]
    hp: int = 200
    attack: int = 3


@dataclass
class Elf(Player):
    pass


@dataclass
class Goblin(Player):
    pass


def load_data(path):
    with open(path) as f:
        rows = f.read().strip().split("\n")

    map_ = {}

    for r, row in enumerate(rows):
        for c, char in enumerate(row):
            if char == "E":
                map_[(r, c)] = Elf((r, c))
            elif char == "G":
                map_[(r, c)] = Goblin((r, c))
            else:
                map_[(r, c)] = char

    return map_


def bfs(start, targets, map_):
    queue = deque([(0, 0, start)])
    distances = {start: 0}

    while queue:
        n, steps, loc = queue.popleft()

        if loc in targets:
            return distances

        for i, nbr in enumerate(get_neighbours(loc)):
            if nbr not in distances and (map_[nbr] == "." or nbr in targets):
                next_steps = 4 * steps + i
                queue.append((n + 1, next_steps, nbr))
                distances[nbr] = (n + 1, next_steps)

    return None


def get_neighbours(loc):
    # yield neighbours in reading order
    for dr, dc in ((-1, 0), (0, -1), (0, 1), (1, 0)):
        yield (loc[0] + dr, loc[1] + dc)


def parse_steps(n, steps):
    dirs = ((-1, 0), (0, -1), (0, 1), (1, 0))
    out = []
    for _ in range(n):
        out.append(steps % 4)
        steps //= 4
    return [dirs[x] for x in reversed(out)]


def simulate(map_, end_on_elf_death=False):
    rounds = 0
    while True:
        players = {k for k, v in map_.items() if isinstance(v, Player)}
        for player in sorted(players):
            if player not in players:
                # player died...
                continue

            # identify targets
            targets = [
                target
                for target in players
                if not isinstance(map_[target], type(map_[player]))
            ]

            if not targets:
                # if no targets, play ends
                return (
                    sum(
                        player.hp
                        for player in map_.values()
                        if isinstance(player, Player)
                    )
                    * rounds
                )

            if not (set(targets) & set(get_neighbours(player))):
                # no targets in range, take a step
                distances = bfs(player, targets, map_)
                if distances is not None:
                    # get nearest reachable neighbour of target
                    # if there's a tie, order by reading order
                    _, dest = min(
                        (
                            (distances.get(nbr, (float("inf"), None))[0], nbr)
                            for target in targets
                            for nbr in get_neighbours(target)
                            if map_[nbr] == "."
                        ),
                    )
                    n, steps = distances[dest]
                    # parse the first step we should take towards destination
                    step = parse_steps(n, steps)[0]
                    next_loc = (player[0] + step[0], player[1] + step[1])
                    # update the map
                    map_[next_loc] = map_[player]
                    map_[player] = "."
                    players.add(next_loc)
                    players.remove(player)
                    player = next_loc

            if reachable_targets := set(targets) & set(get_neighbours(player)):
                target = min(reachable_targets, key=lambda loc: (map_[loc].hp, loc))
                map_[target].hp -= map_[player].attack
                if map_[target].hp <= 0:
                    if end_on_elf_death and isinstance(map_[target], Elf):
                        return False
                    map_[target] = "."
                    players.remove(target)

        rounds += 1


def part_1(map_):
    return simulate(map_)


def part_2(map_):
    for attack in range(4, 100):
        m = deepcopy(map_)
        for p in m.values():
            if isinstance(p, Elf):
                p.attack = attack

        if res := simulate(m, end_on_elf_death=True):
            return res


if __name__ == "__main__":
    map_ = load_data(sys.argv[1])
    print(f"Part 1: {part_1(deepcopy(map_))}")
    print(f"Part 2: {part_2(map_)}")
