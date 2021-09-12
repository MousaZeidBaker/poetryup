import pytest
import toml
from pytest_mock import MockerFixture


@pytest.fixture(scope="function")
def mock_poetry_commands(mocker: MockerFixture) -> None:
    mocker.patch('poetryup.poetryup._run_poetry_update', return_value=None)

    return_value = "poetryup 0.2.0 Run poetry update and bump versions in pyproject.toml file" \
                   "\n└── toml >=0.10.2,<0.11.0"
    mocker.patch('poetryup.poetryup._run_poetry_show', return_value=return_value)


@pytest.fixture(scope="session")
def pyproject_fixture() -> str:
    return toml.dumps({
        "tool": {
            "poetry": {
                "name": "test-poetryup",
                "version": "0.1.0",
                "description": "Test PoetryUp",
                "authors": ["Mousa Zeid Baker"],
                "dependencies": {"python": "^3.6", "poetryup": "^0.1.0"},
                "dev-dependencies": {},
            }
        },
        "build-system": {
            "requires": ["poetry-core>=1.0.0"],
            "build-backend": "poetry.core.masonry.api",
        },
    })
