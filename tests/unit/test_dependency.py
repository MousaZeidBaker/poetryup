from poetryup.models.dependency import Constraint, Dependency


def test_normalized_name() -> None:
    dependency = Dependency(
        name="poetry_up",
        version="0.1.0",
        group="default",
    )
    assert dependency.normalized_name == "poetry-up"


def test_constraint() -> None:
    dependency = Dependency(
        name="poetryup",
        version="^0.1.0",
        group="default",
    )
    assert dependency.constraint == Constraint.CARET

    dependency = Dependency(
        name="poetryup",
        version="~0.1.0",
        group="default",
    )
    assert dependency.constraint == Constraint.TILDE

    dependency = Dependency(
        name="poetryup",
        version="0.*",
        group="default",
    )
    assert dependency.constraint == Constraint.WILDCARD

    dependency = Dependency(
        name="poetryup",
        version="!=0.1.0",
        group="default",
    )
    assert dependency.constraint == Constraint.INEQUALITY

    dependency = Dependency(
        name="poetryup",
        version="0.1.0",
        group="default",
    )
    assert dependency.constraint == Constraint.EXACT

    dependency = Dependency(
        name="poetryup",
        version=">=0.1.0,<0.2.0",
        group="default",
    )
    assert dependency.constraint == Constraint.MULTIPLE_REQUIREMENTS

    dependency = Dependency(
        name="poetryup",
        version=[
            {"version": "0.1.0", "python": "^2.7"},
            {"version": ">=0.2.0", "python": ">=3.7"},
        ],
        group="default",
    )
    assert dependency.constraint == Constraint.MULTIPLE_CONSTRAINTS
