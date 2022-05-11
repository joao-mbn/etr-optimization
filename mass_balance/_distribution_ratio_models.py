from templates._classes import Proton, Ree
from templates._types import Number


def logD_x_pH(cell_number: int, ree: Ree, proton: Proton) -> Number:
    return proton.cells_concentrations[cell_number] ** -ree.model_coefficients['a'] * 10 ** ree.model_coefficients['b']
