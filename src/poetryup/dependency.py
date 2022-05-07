from typing import Union

from tomlkit import items


class Dependency:
    """A class to represent a dependency

    Args:
        name: The name of the dependency
        version: The version of the dependency
        group: The group of the dependency
    """

    def __init__(
        self,
        name: str,
        version: Union[items.String, items.InlineTable, items.Array],
        group: str,
    ) -> None:
        self.name = name
        self.version = version
        self.group = group

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
