import os
from pathlib import Path

from poetryup.main import poetryup


def pytest_generate_tests(metafunc) -> None:
    input_pyproject_path = os.path.join(
        os.path.dirname(__file__), "fixtures/input_pyproject"
    )
    input_pyprojects = [
        file.read_text() for file in Path(input_pyproject_path).glob("*.toml")
    ]

    expected_pyproject_path = os.path.join(
        os.path.dirname(__file__), "fixtures/expected_pyproject"
    )
    expected_pyprojects = [
        file.read_text()
        for file in Path(expected_pyproject_path).glob("*.toml")
    ]

    argvalues = list(zip(input_pyprojects, expected_pyprojects))
    ids = [file.name for file in Path(input_pyproject_path).glob("*.toml")]

    metafunc.parametrize(
        argnames=("input_pyproject", "expected_pyproject"),
        argvalues=argvalues,
        ids=ids,
    )


def test_poetryup(
    input_pyproject: str, expected_pyproject: str, mock_poetry_commands
) -> None:
    updated_pyproject = poetryup(input_pyproject)
    assert updated_pyproject == expected_pyproject
