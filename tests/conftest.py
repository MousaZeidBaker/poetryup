import pytest
from pytest_mock import MockerFixture

from poetryup.core.pyproject import Pyproject


@pytest.fixture(scope="function")
def mock_poetry_commands(mocker: MockerFixture) -> None:
    """Mock poetry commands"""

    mocker.patch.object(
        Pyproject,
        "_Pyproject__get_poetry_version",
        return_value="1.1.0",
    )

    mocker.patch.object(
        Pyproject,
        "_Pyproject__run_poetry_show",
        return_value=(
            "poetryup 0.2.0 Update dependencies and bump their version in the "
            "pyproject.toml file"
            "\n└── toml >=0.10.2,<0.11.0\n"
            "poetryup-extra 0.2.0 "
            "pyproject.toml file"
            "\n└── toml >=0.10.2,<0.11.0\n"
        ),
    )

    mocker.patch.object(
        Pyproject,
        "_Pyproject__run_poetry_update",
        return_value=None,
    )

    mocker.patch.object(
        Pyproject,
        "_Pyproject__run_poetry_add",
        return_value=None,
    )
