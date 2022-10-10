from packaging import version as version_
from pytest_mock import MockerFixture

from poetryup.core.poetry import Poetry


def test_version_poetry_1_1_x(
    mocker: MockerFixture,
) -> None:
    mocker.patch(
        "poetryup.core.poetry.cmd_run",
        return_value="Poetry version 1.2.3",
    )
    poetry = Poetry()
    assert poetry.version == version_.parse("1.2.3")


def test_version_poetry_1_2_x(
    mocker: MockerFixture,
) -> None:
    mocker.patch(
        "poetryup.core.poetry.cmd_run",
        return_value="Poetry (version 1.2.3)",
    )
    poetry = Poetry()
    assert poetry.version == version_.parse("1.2.3")
