# post-fetcher

Concurrent async HTTP fetcher built with `httpx` and `asyncio`, managed with `uv`.

## Features

- **Bounded concurrency**: Controls simultaneous requests using an `asyncio.Semaphore`.
- **Retries with backoff & jitter**: Retries failed requests up to 3 times on timeout or HTTP 5xx errors with exponential delay plus randomized jitter.
- **Graceful shutdown**: Traps cancellation signals (`Ctrl+C` / `CancelledError`) and cancels all outstanding tasks before exiting.
- **Dependency injection**: Accepts external `httpx.AsyncClient` instances to make unit testing fast and offline.

---

## Project Structure

```text
post_fetcher/
├── src/
│   └── post_fetcher/
│       ├── __init__.py
│       ├── service.py    # single_service & combined_service logic
│       └── cli.py        # CLI entry point and signal handling
├── tests/
│   ├── __init__.py
│   └── test_service.py   # Unit tests with respx mocks
└── pyproject.toml
```

---

## Getting Started

### Prerequisites

- Python 3.11+ (configured for 3.14+)
- [`uv`](https://docs.astral.sh/uv/)

### Installation

Clone the repo and sync dependencies:

```bash
uv sync
```

### Running the App

Run the CLI command registered in `pyproject.toml`:

```bash
uv run post-fetcher
```

---

## Development

### Running Tests

Tests use `pytest`, `pytest-asyncio`, and `respx` to mock HTTP traffic without making real network requests:

```bash
uv run pytest
```

### Linting and Formatting

Code linting and formatting are handled by `ruff`:

```bash
# Check for lint and import order issues
uv run ruff check

# Auto-fix fixable issues
uv run ruff check --fix

# Format code style
uv run ruff format
```
