import logging
from typing import List, Optional

from packaging import version as version_

from poetryup.core.cmd import cmd_run


class Poetry:
    """A helper class to run poetry commands"""

    @property
    def version(self) -> version_.Version:
        """Return the installed poetry version"""

        output = cmd_run(["poetry", "--version"], capture_output=True)
        # output is: 'Poetry (version x.y.z)'
        version = output.rsplit(" ", 1).pop().strip().replace(")", "")
        return version_.parse(version)

    def show(self) -> str:
        """Run poetry show command

        Returns:
            The output from the poetry show command
        """

        return cmd_run(["poetry", "show", "--tree"], capture_output=True)

    def update(self) -> None:
        """Run poetry update command"""

        cmd_run(["poetry", "update"])

    def add(
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
            cmd_run(["poetry", "add", *packages])
        elif group == "dev" and self.version < version_.parse("1.2.0"):
            cmd_run(["poetry", "add", *packages, f"--{group}"])
        elif self.version >= version_.parse("1.2.0"):
            cmd_run(["poetry", "add", *packages, "--group", group])
        else:
            logging.warning(f"Couldn't add package(s) '{packages}'")
