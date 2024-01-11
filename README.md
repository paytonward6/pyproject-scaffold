[![PyPI version](https://img.shields.io/pypi/v/pyproject-scaffold.svg)](https://pypi.org/project/pyproject-scaffold)

# pyproject-scaffold
Python scaffolding framework that exclusively uses pyproject.toml

## Installation

Install via `python3 -m pip install pyproject-scaffold`

## Usage
> Working directory must be empty prior to using `pyproject-scaffold`

The following files are created when initializing a project (except when used with `--dry-run`):
- `./pyproject.toml`
- `./src/example/main.py`
- `./src/example/__init__.py`

### Simple Usage
`pyproject-scaffold example -d requests Jinja2` will create project titled `example` with the dependencies `requests` and `Jinja2`.

### Optional Dependencies
Using the previous example as a base, we will add use the `-o` option to add optional dependencies. The first argument to `-o` will the variant name, with following arguments being the dependencies to install under that variant. `-o` can be called multiple times to create additional variants.

So, `pyproject-scaffold example -d requests Jinja2 -o dev pytest pytest-mock` will create project titled `example` with the dependencies `requests` and `Jinja2` and the optional-dependencies `pytest` and `pytest-mock` under the `dev` variant.

### Version
`pyproject-scaffold example -v 1.0.0` will create a project with the version set to `1.0.0`. The default for the version is `0.1.0`

### Defaults

`pyproject-scaffold example --defaults` will create a project titled `example` with the following dependencies:
- `pydantic`
- `requests`

and the following optional dependencies under the `dev` variant:
- `pytest`
- `pyfakefs`
- `pytest-mock`

### Dry Run
`pyproject-scaffold example --dry-run` will print the contents of the `pyproject.toml` that would be created; no files or directories will be created.


Run `pyproject-scaffold -h` for a  list of all options.
