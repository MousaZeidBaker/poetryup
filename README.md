# PoetryUp

![build](https://github.com/MousaZeidBaker/poetryup/workflows/Publish/badge.svg)
![test](https://github.com/MousaZeidBaker/poetryup/workflows/Test/badge.svg)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![python_version](https://img.shields.io/badge/python-%3E=3.6-blue.svg)
[![pypi_v](https://img.shields.io/pypi/v/poetryup.svg)](https://pypi.org/project/poetryup)
[![pypi_dm](https://img.shields.io/pypi/dm/poetryup.svg)](https://pypi.org/project/poetryup)

PoetryUp updates dependencies and bumps their version in the `pyproject.toml` file with respect to their version
constraint. The `poetry.lock` file will be recreated as well. PoetryUp runs
[poetry](https://github.com/python-poetry/poetry) commands, thus it's required to be installed. The difference between
running `poetry update` and `poetryup`, is that the latter also modifies the `pyproject.toml` file.

![poetryup_demo](https://raw.githubusercontent.com/MousaZeidBaker/poetryup/master/media/poetryup_demo.gif)

## Usage
```shell
poetryup
```

Run tests
```shell
pytest tests
```

## Contributing
Contributions are welcome via pull requests.

## Issues
If you encounter any problems, please file an [issue](https://github.com/MousaZeidBaker/poetryup/issues) along with a
detailed description.

## Develop
Activate virtual environment
```shell
poetry shell
```

Install dependencies
```shell
poetry install
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
