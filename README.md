# advent-of-code

My solutions to various [advent of code][aoc] problems.
Written for Python 3.13+.

## Generate boilerplate

This repo contains a helper package to generate boilerplate code each day and
fetch data. To use it first follow the instructions for authenticating
[advent-of-code-data][aocd], and installing [uv][uv].

Boilerplate can be generated and data fetched with

```sh
uv run ac
```

or for a specific year and day

```sh
uv run ac 2021 1
```

Specify the location with the `--outdir` option

```sh
uv run ac 2021 1 --outdir path/to/solutions
```

## Linting / formatting code

Code is formatted and linted with `ruff` and `pyright`. There are tasks for running the commands wth [`just`][just]:

```sh
just lint
```

to lint all code and

```sh
just format
```

to fix problems that can be fixed automatically.

[aoc]: http://adventofcode.com/
[aocd]: https://github.com/wimglenn/advent-of-code-data
[just]: https://github.com/casey/just
[uv]: https://docs.astral.sh/uv
