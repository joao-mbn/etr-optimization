import math as m
from typing import Callable, TypeAlias

import numpy as np
from static_values._rees import REE_VALENCY
from scipy.optimize import fsolve
from templates._classes import Proton, Ree
from templates._types import Number, Vector

Rees: TypeAlias = list[Ree]

def solver(distribution_ratio_model: Callable[..., Number], rees: Rees, proton: Proton, ao_ratio: Number, n_cells: int):
    """
    Solves the system of equations for a given isotherm.
    Note 1: Cells are enumerated from 0 to N, so that 10 cells of extration goes from Cell 0 to Cell 9.
    Note 2: Charge Balance assumes that the REE concentrations are in mol/L of the atom.

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
    results: Vector = fsolve(
        create_system_of_equations, guesses, args=(distribution_ratio_model, ao_ratio, n_cells, rees, proton)
    ).tolist()  # type: ignore

    unpack_values(results, n_cells, rees, proton)

def create_system_of_equations(guesses, *args) -> Vector:

    distribution_ratio_model, ao_ratio, n_cells, rees, proton = args
    unpack_values(guesses, n_cells, rees, proton)

    equations: Vector = []
    charge_constant = m.fsum(ree.aq_feed_concentration * ree.valency for ree in rees)

    equations += create_cell_charge_balance_equations(charge_constant, n_cells, rees, proton)
    equations += create_distribution_ratios_equations(distribution_ratio_model, n_cells, rees, proton)

    for cell_number in range(0, n_cells):
        equations += create_cell_mass_balance_equations(cell_number, n_cells, ao_ratio, rees)

    return equations

def create_cell_mass_balance_equations(cell_number: int, n_cells: int, ao_ratio: Number, rees: Rees) -> Vector:
    """Generate mass balance for each ree in a given cell."""
    equations: Vector = []
    for ree in rees:
        if cell_number == 0:   # ree_aq_feed as known simplification
            equation = \
                ree.cells_aq_concentrations[cell_number] * (ree.distribution_ratios[cell_number] + ao_ratio) \
                - ree.cells_aq_concentrations[cell_number + 1] * ree.distribution_ratios[cell_number + 1] \
                - ree.aq_feed_concentration * ao_ratio
        elif cell_number == n_cells - 1:   # ree_org_feed as known simplification
            equation = \
                ree.cells_aq_concentrations[cell_number] * (ree.distribution_ratios[cell_number] + ao_ratio) \
                - ree.org_feed_concentration \
                - ree.cells_aq_concentrations[cell_number - 1] * ao_ratio
        else:   # general equation
            equation = \
                ree.cells_aq_concentrations[cell_number] * (ree.distribution_ratios[cell_number] + ao_ratio) \
                - ree.cells_aq_concentrations[cell_number + 1] * ree.distribution_ratios[cell_number + 1] \
                - ree.cells_aq_concentrations[cell_number - 1] * ao_ratio

        equations.append(equation)

    return equations

def create_cell_charge_balance_equations(charge_constant: Number, n_cells: int, rees: Rees, proton: Proton) -> Vector:
    """Generate charge balance for each cell."""
    equations: Vector = []
    for i in range(0, n_cells):
        equation = charge_constant - proton.cells_concentrations[i] - REE_VALENCY * m.fsum([ree.cells_aq_concentrations[i] for ree in rees])
        equations.append(equation)
    return equations

def create_distribution_ratios_equations(distribution_ratio_model, n_cells: int, rees: Rees, proton: Proton) -> Vector:
    """Generate partition coefficient equations for each cell."""
    equations: Vector = []
    for cell_number in range(0, n_cells):
        for ree in rees:
            equation = ree.distribution_ratios[cell_number] - distribution_ratio_model(cell_number, ree, proton)
            equations.append(equation)

    return equations

def create_guesses(n_cells: int, rees: Rees, proton: Proton) -> Vector:
    guesses: np.ndarray = np.array([])
    for ree in rees:
        guesses = np.concatenate([ guesses, create_ree_guesses(n_cells, ree) ])
        guesses = np.concatenate([ guesses, create_distribution_ratios_guesses(n_cells, ree) ])

    guesses = np.concatenate([ guesses, create_proton_guesses(n_cells, proton) ])

    return guesses.tolist()

def create_ree_guesses(n_cells: int, ree: Ree):
    return np.linspace(ree.aq_feed_concentration, ree.aq_feed_concentration * 0.001, n_cells)

def create_proton_guesses(n_cells: int, proton: Proton):
    return np.linspace(proton.feed_concentration, proton.feed_concentration * 1.2, n_cells)

def create_distribution_ratios_guesses(n_cells: int, ree: Ree):
    return np.linspace(1, 1, n_cells)

def unpack_values(vars: Vector, n_cells: int, rees: Rees, proton: Proton):
    """Unpack guesses into the rees and proton.

    For 2 Rees:

    |---N---|---N---|---N---|---N---|---N---|

      [Ree1]  D_Ree1  [Ree2]  D_Ree2   [H+]

    """
    for i, ree in enumerate(rees):
        ree.cells_aq_concentrations = vars[2 * i * n_cells: (2 * i + 1) * n_cells]
        ree.distribution_ratios = vars[(2 * i + 1) * n_cells: (2 * i + 2) * n_cells]

    proton.cells_concentrations = vars[-n_cells:]
