import os
from pathlib import Path
from unittest.mock import call

from pytest_mock import MockerFixture

from poetryup.core.pyproject import Pyproject

pyproject_str = Path(
    os.path.join(
        os.path.dirname(__file__),
        "fixtures/input_pyproject/pyproject.toml",
    )
).read_text()

expected_pyproject_str = Path(
    os.path.join(
        os.path.dirname(__file__),
        "fixtures/expected_pyproject/pyproject.toml",
    )
).read_text()


def test_update_dependencies(
    mock_poetry_commands,
) -> None:
    pyproject = Pyproject(pyproject_str)
    pyproject.update_dependencies()

    assert pyproject.dumps() == expected_pyproject_str

    table = pyproject.pyproject["tool"]["poetry"]["dependencies"]
    assert table["poetryup"] == "^0.2.0"

    table = pyproject.pyproject["tool"]["poetry"]["group"]["main"][
        "dependencies"
    ]
    assert table["poetryup_tilde"] == "^0.2.0"
    assert table["poetryup_exact"] == "0.2.0"
    assert table["poetryup_restricted"] == {
        "version": "^0.2.0",
        "python": "<3.7",
    }
    assert table["poetryup_git"] == {
        "git": "https://github.com/MousaZeidBaker/poetryup.git"
    }
    assert table["poetryup_underscore"] == "^0.2.0"
    assert table["Poetryup_Capital"] == "^0.2.0"


def test_update_dependencies_latest(
    mock_poetry_commands,
    mocker: MockerFixture,
) -> None:
    pyproject = Pyproject(pyproject_str)
    mock = mocker.patch.object(
        pyproject,
        "_Pyproject__run_poetry_add",
        return_value=None,
    )
    pyproject.update_dependencies(latest=True)

    calls = [
        call(
            packages=["poetryup@latest"],
            group="default",
        ),
        call(
            packages=[
                "poetryup_tilde@latest",
                "poetryup_exact@latest",
                "poetryup_underscore@latest",
                "Poetryup_Capital@latest",
            ],
            group="main",
        ),
    ]
    mock.assert_has_calls(calls)
