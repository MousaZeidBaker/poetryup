import logging
import re
import subprocess
import sys
from typing import Dict, List, Optional, Union

import tomlkit
from packaging import version as version_

from poetryup.models.dependency import Constraint, Dependency


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
        self._dependencies = None  # caches the dependencies

    @property
    def dependencies(self) -> List[Dependency]:
        """The pyproject dependencies"""

        if self._dependencies is not None:
            # return cached dependencies
            return self._dependencies

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

        self._dependencies = dependencies  # cache dependencies
        return dependencies

    @property
    def lock_dependencies(self) -> List[Dependency]:
        """The pyproject dependencies with their lock version"""

        # run poetry show to get currently installed dependencies
        output = self.__run_poetry_show()

        # create dependencies from each line of the output
        pattern = re.compile("^[a-zA-Z-]+")
        lock_dependencies: List[Dependency] = []
        for line in output.split("\n"):
            if pattern.match(line) is None:
                # not a matching line, continue to next
                continue

            # extract name and version
            lock_name, lock_version, *_ = line.split()

            # search for dependency in pyproject
            dependency = self.search_dependency(self.dependencies, lock_name)
            if dependency is None:
                # dependency not found, continue to next
                continue

            lock_dependencies.append(
                Dependency(
                    name=dependency.name,
                    version=lock_version,
                    group=dependency.group,
                )
            )

        return lock_dependencies

    @property
    def bumped_dependencies(self) -> List[Dependency]:
        """The pyproject dependencies with their version bumped to lock version

        Lock versions will be used if applicable. For instance, using the lock
        version for a dependency that is specified with the inequality
        constraint '!=x.y.z' would completely change its meaning.
        """

        lock_dependencies = self.lock_dependencies

        bumped_dependencies: List[Dependency] = []
        for dependency in self.dependencies:
            constraint = dependency.constraint

            # check for dependencies whom version can't be bumped
            if (
                constraint == Constraint.MULTIPLE_CONSTRAINTS
                or constraint == Constraint.MULTIPLE_REQUIREMENTS
                or constraint == Constraint.WILDCARD
            ):
                bumped_dependencies.append(dependency)
                continue

            # search for lock dependency
            lock_dependency = self.search_dependency(
                lock_dependencies,
                dependency.name,
            )
            if lock_dependency is None:
                # lock dependency not found, dependency stays unchanged
                bumped_dependencies.append(dependency)
                continue

            bumped_version = None
            if constraint == Constraint.CARET:
                bumped_version = "^" + lock_dependency.version
            elif constraint == Constraint.TILDE:
                bumped_version = "~" + lock_dependency.version
            elif constraint == Constraint.INEQUALITY:
                version_str = ""
                if isinstance(dependency.version, str):
                    version_str = dependency.version
                elif isinstance(dependency.version, Dict):
                    version_str = dependency.version.get("version", "")

                if version_str[:2] == ">=":
                    bumped_version = ">=" + lock_dependency.version
            elif constraint == Constraint.EXACT:
                bumped_version = lock_dependency.version

            version = dependency.version
            if bumped_version is None:
                # bump version can't be determined, version stays unchanged
                pass
            elif isinstance(version, str):
                version = bumped_version
            elif (
                isinstance(version, Dict) and version.get("version") is not None
            ):
                version["version"] = bumped_version

            bumped_dependencies.append(
                Dependency(
                    name=dependency.name,
                    version=version,
                    group=dependency.group,
                )
            )

        return bumped_dependencies

    def dumps(self) -> str:
        """Dumps pyproject into a string."""

        return tomlkit.dumps(self.pyproject)

    def search_dependency(
        self,
        dependencies: List[Dependency],
        name: str,
    ) -> Union[Dependency, None]:
        """Search for a dependency by name given a list of dependencies

        Args:
            dependencies: A list of dependencies to search in
            name: Name of the dependency to search for

        Returns:
            A dependency if found, None if not found
        """

        for dependency in dependencies:
            if dependency.name == name or dependency.normalized_name == name:
                return dependency

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
            for dependency in self.dependencies:
                if skip_exact and dependency.constraint == Constraint.EXACT:
                    # skip dependencies with an exact version
                    continue
                if isinstance(dependency.version, str):
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
        for dependency in self.bumped_dependencies:
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

        if sys.version_info < (3, 7):
            return subprocess.check_output(
                ["poetry", "--version"],
                encoding="UTF-8",
            )

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

        if sys.version_info < (3, 7):
            return subprocess.check_output(
                ["poetry", "show", "--tree"],
                encoding="UTF-8",
            )

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
