import os
from pathlib import Path
from unittest.mock import call

from pytest_mock import MockerFixture

from poetryup.core.pyproject import Pyproject
from poetryup.models.dependency import Constraint, Dependency

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

    table = pyproject.pyproject["tool"]["poetry"]["dependencies"]
    assert table["poetryup"] == "^0.2.0"

    table = pyproject.pyproject["tool"]["poetry"]["group"]["main"][
        "dependencies"
    ]
    assert table["poetryup_caret"] == "^0.2.0"
    assert table["poetryup_tilde"] == "~0.2.0"
    assert table["poetryup_wildcard"] == "*"
    assert table["poetryup_inequality_greater_than"] == ">0.1.0"
    assert table["poetryup_inequality_greater_than_or_equal"] == ">=0.2.0"
    assert table["poetryup_inequality_less_than"] == "<0.1.0"
    assert table["poetryup_inequality_less_than_or_equal"] == "<=0.1.0"
    assert table["poetryup_inequality_not_equal"] == "!=0.1.0"
    assert table["poetryup_exact"] == "0.2.0"
    assert table["poetryup_multiple_requirements"] == ">=0.1.0,<0.2.0"
    assert table["poetryup_multiple_constraints"] == [
        {"version": "0.1.0", "python": "^2.7"},
        {"version": ">=0.2.0", "python": ">=3.7"},
    ]
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
                "poetryup_caret@latest",
                "poetryup_tilde@latest",
                "poetryup_wildcard@latest",
                "poetryup_inequality_greater_than@latest",
                "poetryup_inequality_greater_than_or_equal@latest",
                "poetryup_inequality_less_than@latest",
                "poetryup_inequality_less_than_or_equal@latest",
                "poetryup_inequality_not_equal@latest",
                "poetryup_exact@latest",
                "poetryup_multiple_requirements@latest",
                "poetryup_underscore@latest",
                "Poetryup_Capital@latest",
            ],
            group="main",
        ),
    ]
    mock.assert_has_calls(calls)


def test_update_dependencies_latest_skip_exact(
    mock_poetry_commands,
    mocker: MockerFixture,
) -> None:
    pyproject = Pyproject(pyproject_str)
    mock = mocker.patch.object(
        pyproject,
        "_Pyproject__run_poetry_add",
        return_value=None,
    )
    pyproject.update_dependencies(
        latest=True,
        without_constraints=[Constraint.EXACT],
    )

    calls = [
        call(
            packages=["poetryup@latest"],
            group="default",
        ),
        call(
            packages=[
                "poetryup_caret@latest",
                "poetryup_tilde@latest",
                "poetryup_wildcard@latest",
                "poetryup_inequality_greater_than@latest",
                "poetryup_inequality_greater_than_or_equal@latest",
                "poetryup_inequality_less_than@latest",
                "poetryup_inequality_less_than_or_equal@latest",
                "poetryup_inequality_not_equal@latest",
                # poetryup_exact should not be on the call
                "poetryup_multiple_requirements@latest",
                "poetryup_underscore@latest",
                "Poetryup_Capital@latest",
            ],
            group="main",
        ),
    ]
    mock.assert_has_calls(calls)


def test_update_dependencies_latest_with_specific_group(
    mock_poetry_commands,
    mocker: MockerFixture,
) -> None:
    pyproject = Pyproject(pyproject_str)
    mock = mocker.patch.object(
        pyproject,
        "_Pyproject__run_poetry_add",
        return_value=None,
    )
    pyproject.update_dependencies(latest=True, groups=["main"])

    calls = [
        call(
            packages=[
                "poetryup_caret@latest",
                "poetryup_tilde@latest",
                "poetryup_wildcard@latest",
                "poetryup_inequality_greater_than@latest",
                "poetryup_inequality_greater_than_or_equal@latest",
                "poetryup_inequality_less_than@latest",
                "poetryup_inequality_less_than_or_equal@latest",
                "poetryup_inequality_not_equal@latest",
                "poetryup_exact@latest",
                "poetryup_multiple_requirements@latest",
                "poetryup_underscore@latest",
                "Poetryup_Capital@latest",
            ],
            group="main",
        ),
    ]
    mock.assert_has_calls(calls)


def test_update_dependencies_latest_with_specific_name(
    mock_poetry_commands,
    mocker: MockerFixture,
) -> None:
    pyproject = Pyproject(pyproject_str)
    mock = mocker.patch.object(
        pyproject,
        "_Pyproject__run_poetry_add",
        return_value=None,
    )
    pyproject.update_dependencies(latest=True, names=["poetryup"])

    calls = [
        call(
            packages=["poetryup@latest"],
            group="default",
        ),
    ]
    mock.assert_has_calls(calls)


def test_update_dependencies_latest_with_exclude_names(
    mock_poetry_commands,
    mocker: MockerFixture,
) -> None:
    pyproject = Pyproject(pyproject_str)
    mock = mocker.patch.object(
        pyproject,
        "_Pyproject__run_poetry_add",
        return_value=None,
    )
    pyproject.update_dependencies(
        latest=True, exclude_names=["poetryup_caret", "poetryup"]
    )

    calls = [
        call(
            packages=[
                "poetryup_tilde@latest",
                "poetryup_wildcard@latest",
                "poetryup_inequality_greater_than@latest",
                "poetryup_inequality_greater_than_or_equal@latest",
                "poetryup_inequality_less_than@latest",
                "poetryup_inequality_less_than_or_equal@latest",
                "poetryup_inequality_not_equal@latest",
                "poetryup_exact@latest",
                "poetryup_multiple_requirements@latest",
                "poetryup_underscore@latest",
                "Poetryup_Capital@latest",
            ],
            group="main",
        ),
    ]
    mock.assert_has_calls(calls)


def test_search_dependency(
    mock_poetry_commands,
) -> None:
    pyproject = Pyproject(pyproject_str)
    expected = pyproject.dependencies[0]
    actual = pyproject.search_dependency(
        pyproject.dependencies,
        expected.name,
    )
    assert actual == expected


def test_search_dependency_by_normalized_name(
    mock_poetry_commands,
) -> None:
    pyproject = Pyproject(pyproject_str)
    expected = pyproject.dependencies[0]
    actual = pyproject.search_dependency(
        pyproject.dependencies,
        expected.normalized_name,
    )
    assert actual == expected


def test_search_dependency_non_existent(
    mock_poetry_commands,
) -> None:
    pyproject = Pyproject(pyproject_str)
    assert (
        pyproject.search_dependency(
            pyproject.dependencies,
            "non_existent",
        )
        is None
    )


def test_filter_dependencies_without_constraint(
    mock_poetry_commands,
) -> None:
    dependencies = [
        Dependency(
            name="poetryup_exact",
            version="0.1.0",
            group="default",
        ),
        Dependency(
            name="poetryup_caret",
            version="^0.1.0",
            group="dev",
        ),
    ]
    pyproject = Pyproject(pyproject_str)
    expected = dependencies[1]
    actual = pyproject.filter_dependencies(
        dependencies=dependencies,
        without_constraints=[Constraint.EXACT],
    )
    assert actual == [expected]


def test_filter_dependencies_name(
    mock_poetry_commands,
) -> None:
    dependencies = [
        Dependency(
            name="poetryup_exact",
            version="0.1.0",
            group="default",
        ),
        Dependency(
            name="poetryup_caret",
            version="^0.1.0",
            group="dev",
        ),
    ]
    pyproject = Pyproject(pyproject_str)
    expected = dependencies[0]
    actual = pyproject.filter_dependencies(
        dependencies=dependencies,
        names=[expected.name],
    )
    assert actual == [expected]


def test_filter_dependencies_group(
    mock_poetry_commands,
) -> None:
    dependencies = [
        Dependency(
            name="poetryup_exact",
            version="0.1.0",
            group="default",
        ),
        Dependency(
            name="poetryup_caret",
            version="^0.1.0",
            group="dev",
        ),
    ]
    pyproject = Pyproject(pyproject_str)
    expected = dependencies[0]
    actual = pyproject.filter_dependencies(
        dependencies=dependencies,
        groups=[expected.group],
    )
    assert actual == [expected]


def test_dumps(
    mock_poetry_commands,
) -> None:
    pyproject = Pyproject(pyproject_str)
    pyproject.update_dependencies()

    assert pyproject.dumps() == expected_pyproject_str
