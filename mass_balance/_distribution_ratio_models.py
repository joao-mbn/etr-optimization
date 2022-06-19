from templates._classes import Proton, Ree
from templates._types import Number


def logD_x_pH(ree: Ree, proton_concentration: Number) -> Number:
    """
    Model that relates the logarithm of distribution ratio to pH, converted to its non-logarithmical form.

    log_10(D) = a pH + b
    D = [H+]^-a * 10^b

    """
    return proton_concentration ** -ree.model_coefficients['a'] * 10 ** ree.model_coefficients['b']
