from typing import TypeAlias, TypeVar
from pint import Quantity

Number: TypeAlias = float | int
Scalar: TypeAlias = Quantity[Number]
Vector: TypeAlias = list[Number]
T = TypeVar('T')
Z = TypeVar('Z')