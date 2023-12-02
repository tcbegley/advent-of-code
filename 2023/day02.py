import sys
from dataclasses import dataclass


@dataclass
class Reveal:
    red: int = 0
    green: int = 0
    blue: int = 0


@dataclass
class Game:
    id: int
    reveals: list[Reveal]


def parse_reveal(reveal: str) -> Reveal:
    kwargs = {}
    for item in reveal.split(", "):
        count, colour = item.strip().split(" ")
        kwargs[colour] = int(count)
    return Reveal(**kwargs)


def process_row(row: str) -> list[Game]:
    game, reveals = row.split(": ")
    id_ = int(game[5:])
    reveals = [parse_reveal(reveal) for reveal in reveals.split(";")]
    return Game(id=id_, reveals=reveals)


def load_games(path: str) -> list[Game]:
    with open(path) as f:
        games = f.read().strip().split("\n")
    return [process_row(row) for row in games]


def part_1(games: list[Game]) -> int:
    # how many games are possible if 12 red, 13 green, 14 blue
    return sum(
        game.id
        for game in games
        if all(
            reveal.red <= 12 and reveal.green <= 13 and reveal.blue <= 14
            for reveal in game.reveals
        )
    )


def min_power(game: Game) -> int:
    # the smallest possible number of each colour is the largest value observed
    # in all of the reveals
    min_red = max(reveal.red for reveal in game.reveals)
    min_green = max(reveal.green for reveal in game.reveals)
    min_blue = max(reveal.blue for reveal in game.reveals)

    return min_red * min_green * min_blue


def part_2(games: list[Game]) -> int:
    # what is the sum of powers of the minimum possible collection of cubes
    # in each game
    return sum(map(min_power, games))


if __name__ == "__main__":
    games = load_games(sys.argv[1])
    print(f"Part 1: {part_1(games)}")
    print(f"Part 2: {part_2(games)}")
