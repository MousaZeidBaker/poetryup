from dataclasses import dataclass
from typing import Dict, List, Union


@dataclass(frozen=True)
class Dependency:
    """A class to represent a dependency

    Args:
        name: The name of the dependency
        version: The version of the dependency
        group: The group of the dependency
    """

    name: str
    version: Union[str, Dict, List]
    group: str

    @property
    def normalized_name(self) -> str:
        # https://www.python.org/dev/peps/pep-0503/#normalized-names
        return self.name.replace("_", "-").lower()

    @property
    def constraint(self) -> str:
        if isinstance(self.version, str):
            if self.version[0].startswith(("^", "~")):
                return self.version[0]
        elif isinstance(self.version, Dict):
            if self.version.get("version", "").startswith(("^", "~")):
                return self.version["version"][0]
        return ""  # dependencies with exact version or multiple versions
