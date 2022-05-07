from dataclasses import dataclass
from typing import Union

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
