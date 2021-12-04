import datetime
from pathlib import Path
from typing import Optional

import aocd
import typer

HERE = Path(".")
TEMPLATE = r"""import sys


def load_data(path):
    with open(path) as f:
        return f.read().strip().split("\n")


def part_1(data):
    pass


def part_2(data):
    pass


if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")
"""

app = typer.Typer()


@app.command()
def lets_go(
    year: Optional[int] = typer.Argument(None),
    day: Optional[int] = typer.Argument(None),
):
    if year is None or day is None:
        today = datetime.date.today()
        year = year or today.year
        day = day or today.day

    typer.echo(f"Creating template for {year} day {day}")

    source_dir = HERE / str(year)
    data_dir = source_dir / "data"

    data_dir.mkdir(exist_ok=True, parents=True)

    source_file = source_dir / f"day{day:02d}.py"
    if not source_file.exists():
        source_file.write_text(TEMPLATE)
    else:
        typer.echo(
            typer.style("File exists: ", fg=typer.colors.RED, bold=True)
            + f"file {source_file.name} already exists, not overwriting..."
        )

    data = aocd.get_data(day=day, year=year)
    data_file = data_dir / f"{day}.txt"
    if not data_file.exists():
        data_file.write_text(data)
    else:
        typer.echo(
            typer.style("File exists: ", fg=typer.colors.RED, bold=True)
            + f"file data/{data_file.name} already exists, not overwriting..."
        )
