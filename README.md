# advent-of-code

My solutions to various [advent of code](http://adventofcode.com/) problems.
Written for Python 3.10+.

## Generate boilerplate

This repo contains a helper package to generate boilerplate code each day and
fetch data. To use it first follow the instructions for authenticating
[advent-of-code-data][aocd], and [uv][uv].

Boilerplate can be generated and data fetched with

```sh
uv run aoc
```

or for a specific year and day

```sh
uv run aoc 2021 1
```

Specify the location with the `--outdir` option

```sh
uv run aoc 2021 1 --outdir path/to/solutions
```

## Linting / formatting code

Code is formatted and linted with `ruff` and `pyright`. Run

```sh
uv run ruff check
uv run ruff format --check
uv run pyright .
```

to lint all code and

```sh
uv run ruff check --fix
uv run ruff format
```

to fix problems that can be fixed automatically.

[aocd]: https://github.com/wimglenn/advent-of-code-data
[uv]: https://docs.astral.sh/uv
