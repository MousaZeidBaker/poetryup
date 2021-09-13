#!/usr/bin/env python

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List

import tomlkit
from poetryup import utils
from tomlkit.toml_document import TOMLDocument


@dataclass
class Dependency:
    name: str
    version: str


def _run_poetry_update() -> None:
    """Run poetry update command
    """

    subprocess.run(["poetry", "update"])


def _run_poetry_show() -> str:
    """Run poetry show command

    Returns:
        str: The output from the poetry show command
    """

    return subprocess.run(
        ["poetry", "show", "--tree"],
        capture_output=True
    ).stdout.decode()


def _list_dependencies() -> List[Dependency]:
    """List all top-level dependencies

    Returns:
        List[Dependency]: A list of dependencies
    """

    output = _run_poetry_show()

    dependencies: List[Dependency] = []
    for line in output.split("\n"):
        if re.match("^[a-zA-Z]+", line) is not None:
            name, version, *_ = line.split()
            dependency = Dependency(name=name, version=version)
            dependencies.append(dependency)

    return dependencies


def _bump_versions_in_pyproject(dependencies: List[Dependency], pyproject: TOMLDocument) -> TOMLDocument:
    """Bump versions in pyproject

    Args:
        dependencies (List[Dependency]): A list of dependencies
        pyproject (TOMLDocument): The pyproject file parsed as a TOMLDocument

    Returns:
        TOMLDocument: The updated pyproject
    """

    for dependency in dependencies:
        value = utils.lookup_tomlkit_table(
            table=pyproject["tool"]["poetry"],
            key=dependency.name
        )

        if value.startswith(("^", "~")):
            new_version = value[0] + dependency.version
            utils.update_tomlkit_table(
                table=pyproject["tool"]["poetry"],
                key=dependency.name,
                new_value=new_version
            )

    return pyproject


def poetryup(pyproject_str: str) -> str:
    """Update dependencies and bump their version
    Args:
        pyproject_str (str): The pyproject file parsed as a string

    Returns:
        str: The updated pyproject string
    """

    _run_poetry_update()
    dependencies = _list_dependencies()
    pyproject = tomlkit.loads(pyproject_str)
    updated_pyproject = _bump_versions_in_pyproject(dependencies, pyproject)

    return tomlkit.dumps(updated_pyproject)


def main():
    # read pyproject.toml file
    try:
        pyproject_str = Path("pyproject.toml").read_text()
    except FileNotFoundError:
        raise Exception("poetryup could not find a pyproject.toml file in current directory")

    updated_pyproject_str = poetryup(pyproject_str)
    Path("pyproject.toml").write_text(updated_pyproject_str)


if __name__ == "__main__":
    main()
