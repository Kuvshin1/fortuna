from typing import TypeVar

T = TypeVar('T')


def filter_nullable_values_from_dict(dictionary: dict[str, T | None]) -> dict[str, T]:
    return {key: value for [key, value] in dictionary.items() if value is not None}
