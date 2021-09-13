import pytest
from pytest_mock import MockerFixture


@pytest.fixture(scope="function")
def mock_poetry_commands(mocker: MockerFixture) -> None:
    mocker.patch("src.poetryup.poetryup._run_poetry_update", return_value=None)

    return_value = "poetryup 0.2.0 Run poetry update and bump versions in pyproject.toml file" \
                   "\n└── toml >=0.10.2,<0.11.0"
    mocker.patch("src.poetryup.poetryup._run_poetry_show", return_value=return_value)
