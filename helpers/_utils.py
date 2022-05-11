from typing import Any
from templates._types import T, Z, Number, Vector


def default_if_none(a: T, b: Z) -> T | Z:
    return a if a is not None else b

def value_or_default(dictionary: dict, key: str, default: Z) -> Any | Z:
    return dictionary[key] if key in dictionary else default

def flatten(list_of_lists: list[list[T]]) -> list[T]:
    return [item for internal_list in list_of_lists for item in internal_list]

def is_residue(value: Number, referencial: Number, tolerance: Number = 1e-4) -> bool:
    return True if abs(value / referencial) < tolerance else False

def weighted_average(values: Vector, weights: Vector) -> Number:
    return sum(value * weight for value, weight in zip(values, weights)) / sum(weights)