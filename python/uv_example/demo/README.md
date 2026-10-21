# Python Project with `uv` Guide & Best Practices

A quick-start and reference guide for managing Python projects using [**uv**](https://docs.astral.sh/uv/) — an extremely fast Python package and project manager written in Rust by Astral.

---

## Table of Contents
1. [Quickstart: Running This Project](#quickstart-running-this-project)
2. [Essential `uv` Commands](#essential-uv-commands)
   - [Project Initialization](#1-project-initialization)
   - [Managing Dependencies](#2-managing-dependencies)
   - [Running Scripts & Commands](#3-running-scripts--commands)
   - [Syncing & Lockfiles](#4-syncing--lockfiles)
   - [Managing Python Versions](#5-managing-python-versions)
   - [Running CLI Tools with `uvx`](#6-running-cli-tools-with-uvx)
3. [Understanding `pyproject.toml`](#understanding-pyprojecttoml)
4. [Best Practices](#best-practices)

---

## Quickstart: Running This Project

Clone or navigate to this folder and run:

```bash
# 1. Install dependencies and synchronize virtual environment
uv sync

# 2. Run the configured project entry point ("demo")
uv run demo

# Or run any Python script directly inside the project environment
uv run python -c "import demo; demo.main()"
```

---

## Essential `uv` Commands

### 1. Project Initialization
| Command | Description |
| :--- | :--- |
| `uv init` | Initializes a new project in the current directory with `pyproject.toml`. |
| `uv init my-project` | Creates a new directory `my-project` with project scaffolding. |
| `uv init --app` | Creates an application project (default entry point `main.py`). |
| `uv init --lib` | Creates a package/library project with a `src/` layout. |

### 2. Managing Dependencies
| Command | Description |
| :--- | :--- |
| `uv add <package>` | Adds a dependency to `pyproject.toml`, updates `uv.lock`, and installs it into `.venv`. |
| `uv add <package>@latest` | Adds the latest release of a package. |
| `uv add --dev <package>` | Adds a development dependency (e.g., `pytest`, `ruff`, `mypy`). |
| `uv remove <package>` | Removes a dependency from `pyproject.toml` and `.venv`. |
| `uv remove --dev <package>`| Removes a development dependency. |
| `uv tree` | Displays a visual tree of installed dependencies and transitive dependencies. |

### 3. Running Scripts & Commands
`uv run` runs commands within the context of the project's virtual environment **without requiring manual virtualenv activation**.

```bash
# Run a registered console script defined in [project.scripts]
uv run demo

# Run a specific Python script file
uv run main.py

# Run Python interpreter or one-liner
uv run python -c "import numpy; print(numpy.__version__)"

# Run test runner or linter
uv run pytest
uv run ruff check
```

### 4. Syncing & Lockfiles
| Command | Description |
| :--- | :--- |
| `uv lock` | Resolves dependencies and writes/updates `uv.lock` without installing packages. |
| `uv sync` | Ensures `.venv` matches `uv.lock` exactly (installs missing packages, removes stale ones). |
| `uv sync --frozen` | Syncs without updating `uv.lock` (ideal for CI/CD pipelines). |
| `uv sync --all-extras` | Installs project dependencies along with all optional extra groups. |

### 5. Managing Python Versions
`uv` can download, install, and manage standalone Python toolchains automatically without needing `pyenv` or manual installers:

```bash
# List available and installed Python versions
uv python list

# Install a specific Python version
uv python install 3.12

# Pin Python version for the current project (creates .python-version)
uv python pin 3.12
```

### 6. Running CLI Tools with `uvx`
`uvx` (or `uv tool run`) lets you execute standalone Python command-line tools in temporary, isolated environments without installing them into your project:

```bash
uvx ruff check .
uvx black .
uvx cowsay "Hello from UV!"
```

---

## Understanding `pyproject.toml`

The `pyproject.toml` file is the standardized single source of truth for your Python project. Below is an example breakdown:

```toml
[project]
name = "demo"
version = "0.1.0"
description = "A demo project using uv"
readme = "README.md"
authors = [
    { name = "Your Name", email = "your.email@example.com" }
]
# Minimum Python version required
requires-python = ">=3.12"

# Runtime dependencies (added via `uv add <pkg>`)
dependencies = [
    "numpy>=2.0.0",
]

# Command-line entry points (run with: uv run demo)
[project.scripts]
demo = "demo:main"

# Development-only dependencies (added via `uv add --dev <pkg>`)
[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "ruff>=0.3.0",
]

# Build system definition (using uv's high-speed build backend)
[build-system]
requires = ["uv_build>=0.13.4,<0.14.0"]
build-backend = "uv_build"
```

### Script Syntax Breakdown
In `[project.scripts]`:
```toml
demo = "demo:main"
# ^^^    ^^^^ ^^^^
#  |       |    |--> function name to call
#  |       +-------> python module (e.g. src/demo/__init__.py or demo.py)
#  +---------------> command name you type after `uv run`
```

---

## Best Practices

### 1. Always Commit `uv.lock`
- Keep `uv.lock` checked into Git version control.
- This guarantees 100% reproducible environments across team members, operating systems, and CI/CD pipelines.

### 2. Prefer `uv run` Over Manual `.venv` Activation
- Avoid `source .venv/bin/activate` or `.venv\Scripts\activate` when working with `uv`.
- Running `uv run <command>` automatically uses the project virtual environment, auto-rebuilds when files change, and prevents environment mismatch warnings (`VIRTUAL_ENV does not match...`).

### 3. Separate Production and Development Dependencies
- Use `uv add <pkg>` only for packages required in production.
- Use `uv add --dev <pkg>` for linters, formatters, test runners, and documentation tools (`ruff`, `pytest`, `mypy`).

### 4. CI/CD Reproducibility
In CI/CD environments (GitHub Actions, GitLab CI, etc.), use the `--frozen` flag to prevent unexpected lockfile modifications:
```bash
uv sync --frozen
uv run pytest
```

### 5. Cleaning Up Environment
If dependencies get out of sync or stale packages remain:
```bash
# Reset environment to match uv.lock strictly
uv sync --exact
```
