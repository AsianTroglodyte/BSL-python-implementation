# Python BSL Interpreter

Beginning Student Language (BSL) is a Lisp dialect used to teach programming in
*How to Design Programs*.

This project implements a BSL interpreter in Python as a package.

## Requirements

- Python `>= 3.14`
- One of:
  - [`uv`](https://docs.astral.sh/uv/)
  - `pip` + `venv`

## Project Layout

- Package source: `src/bsl`
- Tests: `tests`
- Entry point:
  - module: `python -m bsl`
  - script: `bsl`

## Run From The Repository (Recommended for development)

### Option A: `uv`

From the repo root:

```bash
uv sync
uv run bsl
```

Equivalent module form:

```bash
uv run python -m bsl
```

Run tests:

```bash
uv run pytest
```

### Option B: `pip` + virtual environment

From the repo root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Run:

```bash
bsl
```

or:

```bash
python -m bsl
```

Run tests:

```bash
python -m pytest
```

## Run From Outside The Repository

### Option A: `uv` without global install

Use `--project` to point to the repo:

```bash
uv run --project /absolute/path/to/BSL_interpreter bsl
```

or:

```bash
uv run --project /absolute/path/to/BSL_interpreter python -m bsl
```

### Option B: install as a reusable command

Install with `uv`:

```bash
uv tool install /absolute/path/to/BSL_interpreter
```

Then run from anywhere:

```bash
bsl
```

Install with `pip` (in a chosen environment):

```bash
python -m pip install /absolute/path/to/BSL_interpreter
```

Then run:

```bash
bsl
```

## Usage

- Start REPL:
  - `bsl` (no args)
- Run a file:
  - `bsl path/to/program.bsl`

## Developer Notes

- Internal package modules use package-aware imports.
- Tests use absolute package imports (`from bsl...`).
- Run package code as modules/scripts (`python -m bsl` or `bsl`), not by
  executing internal files directly (for example, avoid `python src/bsl/scanner.py`).

## Troubleshooting

- `ModuleNotFoundError: No module named 'bsl'`
  - Ensure the package is installed in your environment:
    - `uv sync` (uv workflow), or
    - `python -m pip install -e .` (pip workflow)
- `bsl: command not found`
  - If using venv, activate it first.
  - Ensure you installed the project in the same Python environment you are using.
