from numbers import Number
#from types import Vector, Rees

import numpy as np

from scipy.optimize import fsolve
from classes import Proton, Ree

from constants import REE_VALENCY

Vector = list[Number]
Rees = list[Ree]

def solver(partition_coefficient_model, rees, proton, ao_ratio, n_cells):
    """
    Solves the system of equations for a given isotherm.
    Note: Cells are enumerated from 0 to N, so that 10 cells of extration goes from Cell 0 to Cell 9.

    [Input]:
        - Nº of cells
        - A/O ratio
        - initial pH
        - initial aqueous concentration for each ree
        - initial organic concentration for each ree

    [Output]:
        - aqueous concentration for each ree for each cell
        - organic concentration for each ree for each cell
        - pH for each cell
        - D for each ree for each cell
    """
    guesses = create_guesses(n_cells, rees, proton)
    results = fsolve(create_system_of_equations, guesses, args=(partition_coefficient_model, ao_ratio, n_cells, rees, proton))
    return organize_results(results, n_cells, rees, proton)

def create_system_of_equations(guesses, *args) -> Vector:

    partition_coefficient_model, ao_ratio, n_cells, rees, proton = args
    unpack_values(guesses, n_cells, rees, proton)

    equations: Vector = []
    charge_constant = get_total_charges([ree.aq_feed_concentration for ree in rees], proton.feed_concentration)

    equations += create_cell_charge_balance_equations(charge_constant, n_cells, rees, proton)
    equations += create_partition_coefficient_equations(partition_coefficient_model, n_cells, rees, proton)

    for cell_number in range(0, n_cells):
        equations += create_cell_mass_balance_equations(cell_number, n_cells, ao_ratio, rees)

    return equations

def get_total_charges(ree_initial_concentrations: Vector, proton_initial_concentration: Number) -> float:
    """ From initial [H+] and sum([REE 3+]) values, gets total charge concentration on the solution."""
    return proton_initial_concentration + REE_VALENCY * sum(ree_initial_concentrations)

def create_cell_mass_balance_equations(cell_number: int, n_cells: int, ao_ratio: Number, rees: Rees) -> Vector:
    """Generate mass balance for each ree in a given cell."""
    equations: Vector = []
    for ree in rees:
        if cell_number == 0:   # ree_aq_feed as known simplification
            equation = \
                ree.cells_aq_concentrations[cell_number] * (ree.partition_coefficients[cell_number] + ao_ratio) \
                - ree.cells_aq_concentrations[cell_number + 1] * ree.partition_coefficients[cell_number + 1] \
                - ree.aq_feed_concentration * ao_ratio
        elif cell_number == n_cells - 1:   # ree_org_feed as known simplification
            equation = \
                ree.cells_aq_concentrations[cell_number] * (ree.partition_coefficients[cell_number] + ao_ratio) \
                - ree.org_feed_concentration \
                - ree.cells_aq_concentrations[cell_number - 1] * ao_ratio
        else:   # general equation
            equation = \
                ree.cells_aq_concentrations[cell_number] * (ree.partition_coefficients[cell_number] + ao_ratio) \
                - ree.cells_aq_concentrations[cell_number + 1] * ree.partition_coefficients[cell_number + 1] \
                - ree.cells_aq_concentrations[cell_number - 1] * ao_ratio

        equations.append(equation)

    return equations

def create_cell_charge_balance_equations(charge_constant: Number, n_cells: int, rees: Rees, proton: Proton) -> Vector:
    """Generate charge balance for each cell."""
    equations: Vector = []
    for i in range(0, n_cells):
        equation = charge_constant - proton.cells_concentrations[i] - REE_VALENCY * sum(ree.cells_aq_concentrations[i] for ree in rees)
        equations.append(equation)
    return equations

def create_partition_coefficient_equations(partition_coefficient_model, n_cells: int, rees: Rees, proton: Proton) -> Vector:
    """Generate partition coefficient equations for each cell."""
    equations: Vector = []
    for cell_number in range(0, n_cells):
        for ree in rees:
            equation = ree.partition_coefficients[cell_number] - partition_coefficient_model(cell_number, ree, proton)
            equations.append(equation)

    return equations

def create_guesses(n_cells: int, rees: Rees, proton: Proton) -> Vector:
    guesses = np.array([])
    for ree in rees:
        guesses = np.concatenate([ guesses, create_ree_guesses(n_cells, ree) ])
        guesses = np.concatenate([ guesses, create_partition_coefficient_guesses(n_cells, ree) ])

    guesses = np.concatenate([ guesses, create_proton_guesses(n_cells, proton) ])

    return guesses.tolist()

def create_ree_guesses(n_cells: int, ree: Ree):
    return np.linspace(ree.aq_feed_concentration, ree.aq_feed_concentration * 0.001, n_cells)

def create_proton_guesses(n_cells: int, proton: Proton):
    return np.linspace(proton.feed_concentration, proton.feed_concentration * 1.2, n_cells)

def create_partition_coefficient_guesses(n_cells, ree: Ree):
    return np.linspace(1, 1, n_cells)

def unpack_values(vars: Vector, n_cells: int, rees: Rees, proton: Proton):
    """Unpack guesses into the rees and proton.

    For 2 Rees:

    |---N---|---N---|---N---|---N---|---N---|

      [Ree1]  D_Ree1  [Ree2]  D_Ree2   [H+]

    """
    for i, ree in enumerate(rees):
        ree.cells_aq_concentrations = vars[2 * i * n_cells: (2 * i + 1) * n_cells]
        ree.partition_coefficients = vars[(2 * i + 1) * n_cells: (2 * i + 2) * n_cells]

    proton.cells_concentrations = vars[-n_cells:]

def organize_results(results: Vector, n_cells: int, rees: Rees, proton: Proton):
    unpack_values(results, n_cells, rees, proton)
    return rees, proton


from partition_coefficient_models import logD_x_pH

dysprosium = Ree(0.00855232467, 'Dysprosium', 372.998, 'Dy', model_coefficients=[3.22552, -0.99999])
holmium = Ree(0.01775799374, 'Holmium', 377.858, 'Ho', model_coefficients=[3.05008, -0.68760])
proton = Proton(0.55)

solver(logD_x_pH, [dysprosium, holmium], proton, ao_ratio=0.6, n_cells=40)