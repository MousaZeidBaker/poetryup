import logging
import re
import subprocess
from dataclasses import dataclass
from typing import List, Optional, Union

import tomlkit
from packaging import version as version_
from tomlkit import items


@dataclass
class Dependency:
    """A class to represent a dependency"""

    name: str
    version: Union[items.String, items.InlineTable, items.Array]
    group: str

    @property
    def normalized_name(self) -> str:
        # https://www.python.org/dev/peps/pep-0503/#normalized-names
        return self.name.replace("_", "-").lower()

    @property
    def constraint(self) -> str:
        if type(self.version) is items.String:
            if self.version[0].startswith(("^", "~")):
                return self.version[0]
        elif type(self.version) is items.InlineTable:
            if self.version.get("version", "").startswith(("^", "~")):
                return self.version["version"][0]
        return ""  # dependencies with exact version or multiple versions


class Pyproject:
    """A class to represent a pyproject.toml configuration file.

    The pyproject.toml was defined in PEP 518 and expanded in PEP 621.
    https://www.python.org/dev/peps/pep-0518/
    https://www.python.org/dev/peps/pep-0621/

    Args:
        pyproject_str: The pyproject.toml file parsed as a string
    """

    def __init__(self, pyproject_str: str) -> None:
        self.pyproject = tomlkit.loads(pyproject_str)
        self.poetry_version = version_.parse(self.__get_poetry_version())

    def dumps(self) -> str:
        """Dumps pyproject into a string."""

        return tomlkit.dumps(self.pyproject)

    def list_dependencies(self) -> List[Dependency]:
        """Returns pyproject dependencies"""

        dependencies: List[Dependency] = []
        table = self.pyproject["tool"]["poetry"]

        # get default dependencies
        for name, version in table.get("dependencies", {}).items():
            if name == "python":
                # ignore python dependency
                continue
            dependency = Dependency(
                name=name,
                version=version,
                group="default",
            )
            dependencies.append(dependency)

        # get dev-dependencies
        for name, version in table.get("dev-dependencies", {}).items():
            dependency = Dependency(
                name=name,
                version=version,
                group="dev",
            )
            dependencies.append(dependency)

        # get dependencies organized in groups
        for group, deps in table.get("group", {}).items():
            for name, version in deps["dependencies"].items():
                dependency = Dependency(
                    name=name,
                    version=version,
                    group=group,
                )
                dependencies.append(dependency)

        return dependencies

    def list_lock_dependencies(self) -> List[Dependency]:
        """Returns pyproject dependencies with their lock version"""

        # create list of lock dependencies
        output = self.__run_poetry_show()
        pattern = re.compile("^[a-zA-Z-]+")
        lock_deps: List[Dependency] = []
        for line in output.split("\n"):
            if pattern.match(line) is not None:
                name, version, *_ = line.split()
                dependency = Dependency(
                    name=name,
                    version=version,
                    group="",
                )
                lock_deps.append(dependency)

        # list dependencies from pyproject and set version to lock version
        dependencies = self.list_dependencies()
        for dependency in dependencies:
            lock_dep = next(
                (
                    lock_dep
                    for lock_dep in lock_deps
                    if lock_dep.normalized_name == dependency.normalized_name
                ),
                None,
            )
            if lock_dep is None:
                logging.info(
                    f"Couldn't find lock dependency for '{dependency.name}'"
                )
                continue

            if type(dependency.version) is items.String:
                dependency.version = dependency.constraint + lock_dep.version
            elif (
                type(dependency.version) is items.InlineTable
                and dependency.version.get("version") is not None
            ):
                dependency.version["version"] = (
                    dependency.constraint + lock_dep.version
                )

        return dependencies

    def update_dependencies(
        self,
        latest: bool = False,
        skip_exact: bool = False,
    ) -> None:
        """Update dependencies and bump their version in pyproject

        Args:
            latest: Whether to update dependencies to their latest version
            skip_exact: Whether to skip dependencies with an exact version
        """

        if latest:
            logging.info("Updating dependencies to their latest version")
            # sort dependencies into their groups and add them at once in order
            # to avoid version solver error in case dependencies depend on each
            # other
            groups = {}
            for dependency in self.list_dependencies():
                if skip_exact and dependency.constraint == "":
                    # skip dependencies with an exact version
                    continue
                if type(dependency.version) is items.String:
                    groups[dependency.group] = groups.get(
                        dependency.group, []
                    ) + [f"{dependency.name}@latest"]

            for group, packages in groups.items():
                self.__run_poetry_add(
                    packages=packages,
                    group=group,
                )
        else:
            logging.info("Running poetry update command")
            self.__run_poetry_update()

        # bump versions in pyproject
        table = self.pyproject["tool"]["poetry"]
        for dependency in self.list_lock_dependencies():
            if dependency.group == "default":
                table["dependencies"][dependency.name] = dependency.version
            elif (
                dependency.group == "dev"
                and table.get("dev-dependencies", {}).get(dependency.name)
                is not None
            ):
                table["dev-dependencies"][dependency.name] = dependency.version
            elif (
                table.get("group", {})
                .get(dependency.group, {})
                .get("dependencies", {})
                .get(dependency.name)
                is not None
            ):
                table["group"][dependency.group]["dependencies"][
                    dependency.name
                ] = dependency.version
            else:
                logging.info(f"Couldn't bump dependency '{dependency.name}'")

    @staticmethod
    def __get_poetry_version() -> str:
        """Return the installed poetry version

        Returns:
            The poetry version installed
        """

        return (
            subprocess.run(
                ["poetry", "--version"],
                capture_output=True,
            )
            .stdout.decode()  # command returns: 'Poetry version x.y.z'
            .rsplit(" ", 1)
            .pop()
            .strip()
        )

    @staticmethod
    def __run_poetry_show() -> str:
        """Run poetry show command

        Returns:
            The output from the poetry show command
        """

        return subprocess.run(
            ["poetry", "show", "--tree"],
            capture_output=True,
        ).stdout.decode()

    @staticmethod
    def __run_poetry_update() -> None:
        """Run poetry update command"""

        subprocess.run(["poetry", "update"])

    def __run_poetry_add(
        self,
        packages: List[str],
        group: Optional[str],
    ) -> None:
        """Run poetry add command

        Args:
            package: The package(s) to add
            group: The group the package(s) should be added to
        """

        if group is None or group == "default":
            subprocess.run(["poetry", "add", *packages])
        elif group == "dev" and self.poetry_version < version_.parse("1.2.0"):
            subprocess.run(["poetry", "add", *packages, f"--{group}"])
        elif self.poetry_version >= version_.parse("1.2.0"):
            subprocess.run(["poetry", "add", *packages, f"--group {group}"])
        else:
            logging.info(f"Couldn't add package(s) '{packages}'")
