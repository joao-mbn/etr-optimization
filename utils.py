from functools import reduce
from _types import Vector, Number, T, Z

def default_to(a: T, b: Z) -> T | Z:
    return a if a is not None else b

def _sum(items: Vector) -> Number:
    return reduce(lambda a, b: a + b, items)

def flatten(list_of_lists: list[list[T]]) -> list[T]:
    return [item for internal_list in list_of_lists for item in internal_list]