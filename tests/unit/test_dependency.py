from tomlkit import container, items

from poetryup.dependency import Dependency


def test_normalized_name() -> None:
    dependency = Dependency(
        name="poetry_up",
        version="0.1.0",
        group="default",
    )
    assert dependency.normalized_name == "poetry-up"


def test_constraint() -> None:
    version = items.String(
        items.StringType.SLB,
        "^0.1.0",
        original="^0.1.0",
        trivia=items.Trivia(),
    )
    dependency = Dependency(
        name="poetry_up",
        version=version,
        group="default",
    )
    assert dependency.constraint == "^"

    version = items.InlineTable(
        value=container.Container(),
        trivia=items.Trivia(),
    )
    version.append("version", "^0.1.0")
    dependency = Dependency(
        name="poetry_up",
        version=version,
        group="default",
    )
    assert dependency.constraint == "^"

    version = items.Array(
        value=[],
        trivia=items.Trivia(),
    )
    dependency = Dependency(
        name="poetry_up",
        version=version,
        group="default",
    )
    assert dependency.constraint == ""
