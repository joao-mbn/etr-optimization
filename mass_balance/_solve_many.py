from typing import Callable

import numpy as np
from helpers._common import (H_from_pH, pH_from_H, are_all_residues, are_results_absurd,
                             classify_rees, g_from_mol, oxide_from_atom,
                             purity, recovery, resolve_cut, separation_factor)
from templates._classes import Proton, Ree
from templates._models import Condition
from templates._types import Number

from mass_balance._solver import solver


def solve_many(cut: str, distribution_ratio_model: Callable[..., Number], rees: list[Ree], proton: Proton,
               max_cells_interval: tuple[int, int], pHi_interval: tuple[Number, Number], ao_ratio_interval: tuple[Number, Number],
               required_raffinate_purity: float = 0.995, minimal_recovery: float = 0.15) -> list[Condition]:

    """
    - Solves the systems of equations for all possible combinations of A/O ratio, Nº of cells and initial pH, \
        given a certain range of investigation and a arbitrary grid that separates one condition of the other.

    - Collects the conditions that meet a minimal criterium of purity.
    - Records data for statiscal analysis in a pivot table.
    """

    approveds: list[Condition] = []
    lighter_fraction, heavier_fraction = resolve_cut(cut)
    rees_of_interest, contaminants = classify_rees(rees, lighter_fraction, heavier_fraction)

    cells_range = np.arange(max_cells_interval[0], max_cells_interval[1] + 1, 1)
    ao_ratio_range = np.arange(ao_ratio_interval[0], ao_ratio_interval[1] + 0.1, 0.1)
    pHi_range = np.arange(pHi_interval[0], pHi_interval[1] + 0.1, 0.1)

    for n_cells in cells_range:
        for ao_ratio in ao_ratio_range:
            for pHi in pHi_range:

                proton.feed_concentration = H_from_pH(pHi)
                solver(distribution_ratio_model, rees, proton, ao_ratio, n_cells)

                if are_results_absurd(rees) or are_all_residues(rees):
                    continue

                purity = calculate_raffinate_purity(rees_of_interest, contaminants)
                recovery, moles_of_ree_product_at_feed, moles_of_ree_product_at_raffinate = calculate_raffinate_recovery(rees_of_interest)

                if purity >= required_raffinate_purity and recovery >= minimal_recovery:

                    separation_factor = calculate_average_border_separation_factor(rees_of_interest[-1], contaminants[0])
                    mass_of_reo_product_at_feed, mass_of_reo_product_at_raffinate = calculate_total_reos(rees_of_interest)
                    pH_at_raffinate = pH_from_H(proton.cells_concentrations[-1])

                    condition_summary = Condition(n_cells, ao_ratio, pHi, purity, recovery, separation_factor,
                                                  mass_of_reo_product_at_feed, mass_of_reo_product_at_raffinate,
                                                  moles_of_ree_product_at_feed, moles_of_ree_product_at_raffinate,
                                                  pH_at_raffinate)
                    approveds.append(condition_summary)

                    clear_result(rees, proton)

    return approveds

def calculate_raffinate_purity(rees_of_interest: list[Ree], contaminants: list[Ree]) -> float:
    rees_of_interest_raffinate_concentration = sum(ree.cells_aq_concentrations[-1] for ree in rees_of_interest)
    contaminants_raffinate_concentration = sum(ree.cells_aq_concentrations[-1] for ree in contaminants)
    return purity(rees_of_interest_raffinate_concentration, contaminants_raffinate_concentration)

def calculate_raffinate_recovery(rees_of_interest: list[Ree]) -> tuple[float, Number, Number]:
    at_feed = sum(ree.aq_feed_concentration for ree in rees_of_interest)
    at_raffinate = sum(ree.cells_aq_concentrations[-1] for ree in rees_of_interest)
    return recovery(at_feed, at_raffinate), at_feed, at_raffinate

def calculate_average_border_separation_factor(upper_lighter, lower_heavier) -> float:
    """
    This calculates the average separation factor between the elements of the cut alone.
    Ex: PrNd/SmEu -> average separation factor Nd/Sm.
    """
    avg_distribution_ratio_of_lighter = np.mean(upper_lighter.distribution_ratios)
    avg_distribution_ratio_of_heavier = np.mean(lower_heavier.distribution_ratios)
    return separation_factor(avg_distribution_ratio_of_lighter, avg_distribution_ratio_of_heavier)

def calculate_total_reos(rees_of_interest: list[Ree]) -> tuple[Number, Number]:
    """
    This calculates the total reos concentration at the feed and at the raffinate.
    A chain conversion is performed from mol/L Ree to g/L Reo.
    """
    mass_of_reo_at_feed = sum(oxide_from_atom(
                                  g_from_mol(ree.aq_feed_concentration, ree.atom_molar_mass),
                                  ree.stoichiometric_proportion, ree.atom_molar_mass, ree.oxide_molar_mass)
                              for ree in rees_of_interest)
    mass_of_reo_at_raffinate = sum(oxide_from_atom(
                                       g_from_mol(ree.cells_aq_concentrations[-1], ree.atom_molar_mass),
                                       ree.stoichiometric_proportion, ree.atom_molar_mass, ree.oxide_molar_mass)
                                   for ree in rees_of_interest)
    return mass_of_reo_at_feed, mass_of_reo_at_raffinate

def clear_result(rees: list[Ree], proton: Proton):
    """
    Since the system yields the results in place, this methods cleans the results, \
        after they were stored elsewhere, to give room for the next system to be solved.
    """
    for ree in rees:
        ree.cells_aq_concentrations = []
        ree.cells_org_concentrations = []
        ree.distribution_ratios = []

    proton.cells_concentrations = []
