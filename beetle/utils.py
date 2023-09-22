"""
Utility class
"""

from typing import Callable, Iterable, TypeVar


T = TypeVar("T")


def is_iterable(value: T):
    """
    test if a value is an iterable or not
    """
    return isinstance(value, (list, tuple))


def is_object(value: T):
    """
    test if value is json object definition
    """
    return isinstance(value, (dict, list, tuple))


def first(iterable: Iterable[T], predicate: Callable[[T], bool]):
    """
    find first in an iterable, returns None if not found
    """
    result = list(filter(predicate, iterable))

    return result[0] if len(result) > 0 else None


def find_by(iterable: Iterable[dict], search: dict, key: str):
    """
    find dict in an iterable by key, returns None if not found
    """

    return first(
        iterable,
        lambda value: value.get(key)
        == search.get(
            key,
            search,
        ),
    )
