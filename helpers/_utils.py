import locale
from math import nan
from typing import Any

from templates._types import Number, T, Vector, Z


def default_if_none(a: T, b: Z) -> T | Z:
    return a if a is not None else b


def value_or_default(dictionary: dict, key: str, default: Z) -> Any | Z:
    return dictionary[key] if key in dictionary else default


def flatten(list_of_lists: list[list[T]]) -> list[T]:
    return [item for internal_list in list_of_lists for item in internal_list]


def is_residue(value: Number, referential: Number, tolerance: Number = 1e-4) -> bool:
    return True if abs(value / referential) < tolerance else False


def weighted_average(values: Vector, weights: Vector) -> Number:
    return sum(value * weight for value, weight in zip(values, weights)) / sum(weights)


def standardize(value: Number, mean: Number, standard_deviation: Number) -> Number:
    return (value - mean) / standard_deviation if standard_deviation != 0 and standard_deviation != nan and type(value) != str else value


def has_any_substring(substrings: list[str], string: str) -> bool:
    return True if any(substring in string for substring in substrings) else False


def format_to_currency(value: Number) -> str:
    locale.setlocale( locale.LC_ALL, 'en_US' )
    return locale.currency(value, grouping = True)
