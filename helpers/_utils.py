from templates._types import T, Z, Number


def default_to(a: T, b: Z) -> T | Z:
    return a if a is not None else b

def flatten(list_of_lists: list[list[T]]) -> list[T]:
    return [item for internal_list in list_of_lists for item in internal_list]

def is_residue(value: Number, referencial: Number, tolerance: Number = 1e-4) -> bool:
    return True if abs(value / referencial) < tolerance else False