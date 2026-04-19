# Contributing

Contributions are welcome! Here's how to get started.

## Setup

```bash
git clone https://github.com/Darius1223/celery-flower-mcp
cd celery-flower-mcp
uv sync
```

## Development workflow

```bash
make fmt        # auto-format
make lint       # lint
make typecheck  # type-check
make test       # run tests
make cov        # tests + coverage
make all        # fmt + lint + typecheck
```

All checks must pass before submitting a PR.

## Adding a new tool

1. Identify the Flower API endpoint in [the docs](https://flower.readthedocs.io/en/latest/api.html)
2. Add the tool to the appropriate module in `source/tools/`
3. Write a test in the corresponding `tests/test_tools_*.py` file
4. Run `make all && make test`

## Submitting a PR

- Keep PRs focused — one feature or fix per PR
- Update `CHANGELOG.md` under `[Unreleased]`
- Ensure CI passes

## Reporting bugs

Open an issue with steps to reproduce, expected vs actual behaviour, and your Flower version.
