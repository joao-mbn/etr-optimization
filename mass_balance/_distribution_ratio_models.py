from templates._classes import Proton, Ree
from templates._types import Number


def logD_x_pH(cell_number: int, ree: Ree, proton: Proton) -> Number:
    """
    Model that relates the logarithm of distribution ratio to pH, converted to its non-logarithmical form.

    log_10(D) = a pH + b
    D = [H+]^-a * 10^b

    """
    return proton.cells_concentrations[cell_number] ** -ree.model_coefficients['a'] * 10 ** ree.model_coefficients['b']
