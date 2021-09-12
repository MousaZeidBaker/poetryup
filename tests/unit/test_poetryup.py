import toml
from poetryup.poetryup import poetryup


def test_poetryup_should_bump_version(pyproject_fixture, mock_poetry_commands) -> None:
    updated_pyproject_str = poetryup(pyproject_fixture)
    updated_pyproject_dict = toml.loads(updated_pyproject_str)
    actual_version = updated_pyproject_dict["tool"]["poetry"]["dependencies"]["poetryup"]
    expected_version = "^0.2.0"
    assert(actual_version == expected_version)
