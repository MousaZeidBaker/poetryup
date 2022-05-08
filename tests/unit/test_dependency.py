from poetryup.models.dependency import Constraint, Dependency


def test_normalized_name() -> None:
    dependency = Dependency(
        name="poetry_up",
        version="0.1.0",
        group="default",
    )
    assert dependency.normalized_name == "poetry-up"


def test_constraint_type() -> None:
    dependency = Dependency(
        name="poetryup",
        version="^0.1.0",
        group="default",
    )
    assert dependency.constraint_type == Constraint.CARET

    dependency = Dependency(
        name="poetryup",
        version="~0.1.0",
        group="default",
    )
    assert dependency.constraint_type == Constraint.TILDE

    dependency = Dependency(
        name="poetryup",
        version="0.*",
        group="default",
    )
    assert dependency.constraint_type == Constraint.WILDCARD

    dependency = Dependency(
        name="poetryup",
        version="!=0.1.0",
        group="default",
    )
    assert dependency.constraint_type == Constraint.INEQUALITY

    dependency = Dependency(
        name="poetryup",
        version="0.1.0",
        group="default",
    )
    assert dependency.constraint_type == Constraint.EXACT

    dependency = Dependency(
        name="poetryup",
        version=">=0.1.0,<0.2.0",
        group="default",
    )
    assert dependency.constraint_type == Constraint.MULTIPLE_REQUIREMENTS

    dependency = Dependency(
        name="poetryup",
        version=[
            {"version": "0.1.0", "python": "^2.7"},
            {"version": ">=0.2.0", "python": ">=3.7"},
        ],
        group="default",
    )
    assert dependency.constraint_type == Constraint.MULTIPLE_CONSTRAINTS
