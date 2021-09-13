#!/usr/bin/env python

from typing import Any, Dict


def lookup_nested_dict(dictionary: Dict, key: str) -> Any:
    """Lookup value recursively in nested dictionary

    Args:
        dictionary (Dict): The dictionary to search in
        key (str): The key to search for

    Returns:
        Any: The value of the key if found, None otherwise
    """

    if key in dictionary:
        return dictionary[key]

    for value in dictionary.values():
        if type(value) is dict:
            lookup = lookup_nested_dict(value, key)
            if lookup is not None:
                return lookup

    return None


def update_nested_dict(dictionary: Dict, key: str, new_value: Any) -> bool:
    """Update value in nested dictionary

    Args:
        dictionary (Dict): The dictionary to search in
        key (str): The key to search for
        new_value (Any): The new value

    Returns:
        Any: True if key found and value updated, False otherwise
    """

    if key in dictionary:
        dictionary[key] = new_value
        return True

    for value in dictionary.values():
        if type(value) is dict:
            updated = update_nested_dict(dictionary=value, key=key, new_value=new_value)
            if updated is True:
                return True

    return False
