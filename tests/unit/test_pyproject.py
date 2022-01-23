import os
from pathlib import Path

from poetryup.pyproject import Pyproject


def pytest_generate_tests(metafunc) -> None:
    input_pyproject_path = os.path.join(
        os.path.dirname(__file__),
        "fixtures/input_pyproject",
    )
    input_pyprojects = [
        file.read_text() for file in Path(input_pyproject_path).glob("*.toml")
    ]

    expected_pyproject_path = os.path.join(
        os.path.dirname(__file__),
        "fixtures/expected_pyproject",
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


def test_update_dependencies(
    input_pyproject: str,
    expected_pyproject: str,
    mock_poetry_commands,
) -> None:
    pyproject = Pyproject(input_pyproject)
    pyproject.update_dependencies()
    assert pyproject.dumps() == expected_pyproject


def test_update_dependencies_latest(
    input_pyproject: str,
    expected_pyproject: str,
    mock_poetry_commands,
) -> None:
    pyproject = Pyproject(input_pyproject)
    pyproject.update_dependencies(latest=True)
    assert pyproject.dumps() == expected_pyproject
