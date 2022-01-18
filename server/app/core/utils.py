"""Imperative Logic for various tasks are contained in this file
If any task can be abstracted into a separete function which does not
pertain to the function of that piece of code, it should be put here.
So that that layer is more declarative
"""

from typing import Any, Dict, List


def find_if_given_keys_exist_in_dict(dict: Dict[str, Any], keys: List[str]) -> bool:
    """Checks if the given keys are present in the dict"""
    isPresent: bool = True

    for key in keys:
        isPresent = isPresent and key in dict and dict.__getitem__(key) is not None

    return isPresent
