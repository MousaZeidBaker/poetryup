# PoetryUp

![build](https://github.com/MousaZeidBaker/poetryup/workflows/Publish/badge.svg)
![test](https://github.com/MousaZeidBaker/poetryup/workflows/Test/badge.svg)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
![python_version](https://img.shields.io/badge/python-%3E=3.6-blue)
[![pypi_v](https://img.shields.io/pypi/v/poetryup)](https://pypi.org/project/poetryup)
[![pypi_dm](https://img.shields.io/pypi/dm/poetryup)](https://pypi.org/project/poetryup)

PoetryUp updates dependencies and bumps their version in both `poetry.lock` as
well as in `pyproject.toml` file. Dependencies version constraints are
respected, unless the `--latest` flag is passed, in which case dependencies will
be updated to their latest available version. PoetryUp runs
[poetry](https://github.com/python-poetry/poetry) commands, thus it's required
to be installed. The difference between running `poetry update` and `poetryup`,
is that the latter also modifies the `pyproject.toml` file.

![poetryup_demo](https://raw.githubusercontent.com/MousaZeidBaker/poetryup/master/media/poetryup_demo.gif)

## Usage
```shell
poetryup --help
```

## Automate Dependency Updates with GitHub Actions
Use PoetryUp with GitHub actions to automate the process of updating
dependencies, for reference see this project's [workflow
configuration](https://github.com/MousaZeidBaker/poetryup/blob/master/.github/workflows/update-dependencies.yaml).

## Contributing
Contributions are welcome via pull requests.

## Issues
If you encounter any problems, please file an
[issue](https://github.com/MousaZeidBaker/poetryup/issues) along with a detailed
description.

## Develop
Activate virtual environment
```shell
poetry shell
```

Install dependencies
```shell
poetry install --remove-untracked
```

Install git hooks
```shell
pre-commit install --hook-type pre-commit
```

Run tests
```shell
pytest tests
```

Run linter
```shell
flake8 .
```

Format code
```shell
black .
```

Sort imports
```shell
isort .
```

Install current project from branch
```shell
poetry add git+https://github.com/MousaZeidBaker/poetryup.git#branch-name
```
