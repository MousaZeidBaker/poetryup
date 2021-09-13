#!/usr/bin/env python

from typing import Any

from tomlkit.container import Table


def lookup_tomlkit_table(table: Table, key: str) -> Any:
    """Lookup value recursively in a tomlkit Table

    Args:
        table (Table): The table to search in
        key (str): The key to search for

    Returns:
        Any: The value of the key if found, None otherwise
    """

    if key in table:
        return table[key]

    for value in table.values():
        if type(value) is Table:
            lookup = lookup_tomlkit_table(table=value, key=key)
            if lookup is not None:
                return lookup

    return None


def update_tomlkit_table(table: Table, key: str, new_value: Any) -> bool:
    """Update value in a tomlkit Table

    Args:
        table (Table): The table to search in
        key (str): The key to search for
        new_value (Any): The new value

    Returns:
        Any: True if key found and value updated, False otherwise
    """

    if key in table:
        table[key] = new_value
        return True

    for value in table.values():
        if type(value) is Table:
            updated = update_tomlkit_table(table=value, key=key, new_value=new_value)
            if updated is True:
                return True

    return False
