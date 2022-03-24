#!/usr/bin/env python

import logging
import os
from pathlib import Path

import typer

from poetryup.pyproject import Pyproject

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO").upper())

app = typer.Typer(add_completion=False)


@app.command()
def poetryup(
    latest: bool = typer.Option(
        default=False,
        help="Whether to update dependencies to their latest version.",
    ),
    skip_exact: bool = typer.Option(
        default=False,
        help="Whether to skip dependencies with an exact version.",
    ),
):
    """Update dependencies and bump their version in pyproject.toml file"""

    try:
        pyproject_str = Path("pyproject.toml").read_text()
    except FileNotFoundError:
        raise Exception(
            "poetryup couldn't find a pyproject.toml file in current directory"
        )

    pyproject = Pyproject(pyproject_str)
    pyproject.update_dependencies(latest, skip_exact)
    Path("pyproject.toml").write_text(pyproject.dumps())


if __name__ == "__main__":
    app()
