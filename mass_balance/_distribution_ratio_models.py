from templates._classes import Proton
from templates._types import Number


def logD_x_pH(cell_number: int, ree, proton: Proton) -> Number:
    return proton.cells_concentrations[cell_number] ** -ree.model_coefficients[0] * 10 ** ree.model_coefficients[1]
