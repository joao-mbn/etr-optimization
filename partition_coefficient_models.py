from classes import Proton


def logD_x_pH(cell_number: int, ree, proton: Proton):
    return proton.cells_concentrations[cell_number] ** -ree.model_coefficients[0] * 10 ** ree.model_coefficients[1]