from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Union


class Constraint(str, Enum):
    # https://python-poetry.org/docs/dependency-specification
    CARET = "caret"
    TILDE = "tilde"
    WILDCARD = "wildcard"
    INEQUALITY = "Inequality"
    EXACT = "exact"
    MULTIPLE_REQUIREMENTS = "multiple_requirements"
    MULTIPLE_CONSTRAINTS = "multiple_constraint"


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

    @property
    def constraint_type(self) -> Constraint:
        if isinstance(self.version, List):
            return Constraint.MULTIPLE_CONSTRAINTS

        version = (
            self.version
            if isinstance(self.version, str)
            else self.version.get("version", "")
        )

        if "," in version:
            return Constraint.MULTIPLE_REQUIREMENTS
        elif version[:1] == "^":
            return Constraint.CARET
        elif version[:1] == "~":
            return Constraint.TILDE
        elif "*" in version:
            return Constraint.WILDCARD
        elif version.startswith((">", "<", ">=", "<=", "!=")):
            return Constraint.INEQUALITY
        elif version[:1].isdigit():
            return Constraint.EXACT
