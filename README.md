# flake8 config

A [Flake8](https://flake8.pycqa.org/en/latest/) config and a plugin to detect **non-ASCII characters** in Python source code, including string literals, docstrings, and comments.

## Features

- Detects non-ASCII characters in:
  - String literals
  - Docstrings (module, class, function)
  - Comments
- Helps enforce code style rules by preventing non-ASCII characters where undesired.
- Compatible with Flake8 7.x and above.

## Installation

You can install directly from GitHub:

```bash
pip install git+https://github.com/fl-gomes/flake8_cfg.git@main
```

## Usage

Run Flake8 as usual on your codebase:

```bash
flake8 path/to/project --config path/to/flake8.cfg
```

### Example output

```plaintext
example.py:10:5: NE001 Non-English characters detected: Привет
```

## Configuration

You can use a Flake8 config file (`.flake8`, `setup.cfg`, or `tox.ini`).

Example `flake8.cfg` config:

```ini
[flake8]
# Maximum line length for the code
max-line-length = 150

# Exclude the .venv folder
exclude = .venv

# Ignore F401 (imported but unused) in __init__.py files
per-file-ignores =
    **/__init__.py: F401,F403

```

## Error Codes

| Code  | Description                             |
|-------|-----------------------------------------|
| NE001 | Non-English characters detected in code |

## Development

Clone the repo and install in editable mode:

```bash
git clone https://github.com/fl-gomes/flake8_cfg.git
cd flake8_cfg
pip install -e .
```
