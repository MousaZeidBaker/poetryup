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

    dependencies = [
        "poetryup",
        "poetryup-caret",
        "poetryup-tilde",
        "poetryup-wildcard",
        "poetryup-inequality-greater-than",
        "poetryup-inequality-greater-than-or-equal",
        "poetryup-inequality-less-than",
        "poetryup-inequality-less-than-or-equal",
        "poetryup-inequality-not-equal",
        "poetryup-exact",
        "poetryup-multiple-requirements",
        "poetryup-multiple-constraints",
        "poetryup-restricted",
        "poetryup-git",
        "poetryup-underscore",
        "poetryup-capital",
    ]
    s = " 0.2.0 Some description\n└── some-package >=0.10.2,<0.11.0\n"
    return_value = s.join(dependencies) + s

    mocker.patch.object(
        Pyproject,
        "_Pyproject__run_poetry_show",
        return_value=return_value,
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
