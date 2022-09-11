#!/usr/bin/env python

import logging
from pathlib import Path
from typing import List

import typer

from poetryup.core.cmd import CommandError, cmd_run
from poetryup.core.pyproject import Pyproject
from poetryup.models.dependency import Constraint

app = typer.Typer(add_completion=False)


def setup_logging(verbosity):
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity > 1:
        level = logging.DEBUG
    logging.basicConfig(level=level)


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
    name: List[str] = typer.Option(
        default=[],
        help="The dependency names to include.",
    ),
    exclude_name: List[str] = typer.Option(
        default=[],
        help="The dependency names to exclude.",
    ),
    group: List[str] = typer.Option(
        default=[],
        help="The dependency groups to include.",
    ),
    verbose: int = typer.Option(
        0,
        "--verbose",
        "-v",
        count=True,
        help='Increase verbosity of messages: "-v" for info, "-vv" for debug.',
    ),
):
    """Update dependencies and bump their version in pyproject.toml file"""
    setup_logging(verbose)

    try:
        pyproject_str = Path("pyproject.toml").read_text()
    except FileNotFoundError:
        raise Exception(
            "poetryup couldn't find a pyproject.toml file in current directory"
        )

    pyproject = Pyproject(pyproject_str)
    without_constraint = [Constraint.EXACT] if skip_exact else []

    try:
        pyproject.update_dependencies(
            latest,
            without_constraint,
            name,
            exclude_name,
            group,
        )
    except CommandError as e:
        raise typer.Exit(e.return_code)

    Path("pyproject.toml").write_text(pyproject.dumps())
    # refresh the lock file after changes in pyproject.toml
    cmd_run(["poetry", "lock", "--no-update"])


if __name__ == "__main__":
    app()
