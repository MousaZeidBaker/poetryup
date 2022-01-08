#!/usr/bin/env python

from typing import Any

from tomlkit import items


def lookup_tomlkit_table(table: items.Table, key: str) -> Any:
    """Lookup value recursively in a tomlkit Table

    Args:
        table (Table): The table to search in
        key (str): The key to search for

    Returns:
        Any: The value of the key if found, None otherwise
    """

    for item_key, item_value in table.items():
        if item_key.lower() == key:
            return item_value

    for value in table.values():
        if type(value) is items.Table:
            lookup = lookup_tomlkit_table(table=value, key=key)
            if lookup is not None:
                return lookup

    return None


def update_tomlkit_table(table: items.Table, key: str, new_value: Any) -> bool:
    """Update value in a tomlkit Table

    Args:
        table (Table): The table to search in
        key (str): The key to search for
        new_value (Any): The new value

    Returns:
        Any: True if key found and value updated, False otherwise
    """

    for item_key, item_value in table.items():
        if item_key.lower() == key:
            table[item_key] = new_value
            return True

    for item_value in table.values():
        if type(item_value) is items.Table:
            updated = update_tomlkit_table(
                table=item_value, key=key, new_value=new_value
            )
            if updated is True:
                return True

    return False
