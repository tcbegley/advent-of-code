lint:
    uv run ruff format --check
    uv run ruff check
    # uv run pyright

format:
    uv run ruff format
    uv run ruff check --fix
