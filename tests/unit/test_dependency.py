from poetryup.dependency import Dependency


def test_normalized_name() -> None:
    dependency = Dependency(
        name="poetry_up",
        version="0.1.0",
        group="default",
    )
    assert dependency.normalized_name == "poetry-up"


def test_constraint() -> None:
    dependency = Dependency(
        name="poetry_up",
        version="^0.1.0",
        group="default",
    )
    assert dependency.constraint == "^"

    dependency = Dependency(
        name="poetry_up",
        version={"version": "^0.1.0"},
        group="default",
    )
    assert dependency.constraint == "^"

    dependency = Dependency(
        name="poetry_up",
        version=[],
        group="default",
    )
    assert dependency.constraint == ""
