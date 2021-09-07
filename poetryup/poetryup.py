#!/usr/bin/env python

import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import toml

from . import utils


@dataclass
class Dependency:
    name: str
    version: str


def _list_dependencies() -> List[Dependency]:
    """List all top-level dependencies

    Returns:
        List[Dependency]: A list of dependencies
    """

    output = subprocess.run(
        ['poetry', 'show', '--tree'],
        capture_output=True
    ).stdout.decode()

    dependencies: List[Dependency] = []
    for line in output.split('\n'):
        if re.match('^[a-zA-Z]+', line) is not None:
            name, version, *_ = line.split()
            dependency = Dependency(name=name, version=version)
            dependencies.append(dependency)

    return dependencies


def _bump_pyproject_versions(dependencies: List[Dependency], pyproject: Dict) -> Dict:
    """Bump versions in pyproject

    Args:
        dependencies (List[Dependency]): A list of dependencies
        pyproject (Dict): The pyproject dictionary

    Returns:
        Dict: The updated pyproject dict
    """

    for dependency in dependencies:
        value = utils.lookup_nested_dict(dictionary=pyproject['tool']['poetry'], key=dependency.name)

        if value.startswith(('^', '~')):
            new_version = value[0] + dependency.version
            utils.update_nested_dict(
                dictionary=pyproject['tool']['poetry'],
                key=dependency.name,
                new_value=new_version
            )

    return pyproject


def poetryup():
    """Run poetry update and bump versions in pyproject.toml file
    """

    # read pyproject.toml file
    try:
        pyproject_string = Path('pyproject.toml').read_text()
    except FileNotFoundError:
        raise Exception('poetryup could not find a pyproject.toml file in current directory')

    pyproject = toml.loads(pyproject_string)

    # run poetry update
    subprocess.run(['poetry', 'update'])
    # list dependencies with their new versions
    dependencies = _list_dependencies()
    # bump versions in pyproject
    pyproject = _bump_pyproject_versions(dependencies, pyproject)

    # create updated pyproject.toml file
    # in order to preserve the order of pyproject.toml, manually append build-system to the end
    build_system = {'build-system': pyproject.pop('build-system')}
    pyproject_string = toml.dumps(pyproject)
    pyproject_string += '\n' + toml.dumps(build_system)

    Path('pyproject.toml').write_text(pyproject_string)


if __name__ == '__main__':
    poetryup()
