from statistics import mean, median
from typing import Any, Callable

import numpy as np
from helpers._common import (H_from_pH, are_all_residues, are_results_absurd,
                             classify_rees, purity, recovery, resolve_cut,
                             separation_factor)
from templates._classes import Proton, Ree
from templates._types import Number

from mass_balance._solver import solver


def solve_many(cut: str, distribution_ratio_model: Callable[..., Number],
               rees: list[Ree], proton: Proton,
               max_cells_interval: tuple[int, int], pHi_interval: tuple[Number, Number],
               ao_ratio_interval: tuple[Number, Number] = (0.5, 2), required_raffinate_purity: float = 0.995):

    approveds: list[Any] = []
    data_to_pivot_table = build_data_to_pivot_table()
    lighter_fraction, heavier_fraction = resolve_cut(cut)
    rees_of_interest, contaminants = classify_rees(rees, lighter_fraction, heavier_fraction)

    cells_range = np.arange(max_cells_interval[0], max_cells_interval[1] + 1)
    ao_ratio_range = np.arange(ao_ratio_interval[0], ao_ratio_interval[1] + 0.1, 0.1)
    pHi_range = np.arange(pHi_interval[0],pHi_interval[1] + 0.05, 0.05)

    for n_cells in cells_range:
        for ao_ratio in ao_ratio_range:
            for pHi in pHi_range:

                proton.feed_concentration = H_from_pH(pHi)
                solver(distribution_ratio_model, rees, proton, ao_ratio, n_cells)

                if are_results_absurd(rees) or are_all_residues(rees):
                    continue

                purity = calculate_raffinate_purity(rees_of_interest, contaminants)
                if purity >= required_raffinate_purity:

                    recovery = calculate_raffinate_recovery(rees_of_interest)
                    separation_factor = calculate_average_border_separation_factor(rees_of_interest[-1], contaminants[0])

                    update_data_to_pivot_table(data_to_pivot_table, purity, recovery, separation_factor)
                    condition_summary = store_condition(n_cells, ao_ratio, pHi, purity, recovery, separation_factor)
                    approveds.append(condition_summary)

                    clear_result(rees, proton)

    data_to_pivot_table['number_of_tests'] = cells_range.__len__() * ao_ratio_range.__len__() * pHi_range.__len__()
    data_to_pivot_table['total_of_approveds'] = approveds.__len__()
    data_to_pivot_table['approved']['average_separation_factor'] = mean([condition['separation_factor'] for condition in approveds])
    data_to_pivot_table['approved']['average_recovery'] = mean([condition['recovery'] for condition in approveds])
    data_to_pivot_table['approved']['separation_factor_median'] = median([condition['separation_factor'] for condition in approveds])
    data_to_pivot_table['approved']['recovery_median'] = median([condition['recovery'] for condition in approveds])

    return data_to_pivot_table, approveds

def calculate_raffinate_purity(rees_of_interest: list[Ree], contaminants: list[Ree]) -> float:
    rees_of_interest_raffinate_concentration = sum(ree.cells_aq_concentrations[-1] for ree in rees_of_interest)
    contaminants_raffinate_concentration = sum(ree.cells_aq_concentrations[-1] for ree in contaminants)
    return purity(rees_of_interest_raffinate_concentration, contaminants_raffinate_concentration)

def calculate_raffinate_recovery(rees_of_interest: list[Ree]) -> float:
    at_feed = sum(ree.aq_feed_concentration for ree in rees_of_interest)
    at_raffinate = sum(ree.cells_aq_concentrations[-1] for ree in rees_of_interest)
    return recovery(at_feed, at_raffinate)

def calculate_average_border_separation_factor(upper_lighter, lower_heavier) -> float:
    avg_distribution_ratio_of_lighter = mean(upper_lighter.distribution_ratios)
    avg_distribution_ratio_of_heavier = mean(lower_heavier.distribution_ratios)
    return separation_factor(avg_distribution_ratio_of_lighter, avg_distribution_ratio_of_heavier)

def build_data_to_pivot_table():
    return {
        'approved': {
            'highest_average_separation_factor': -np.inf,
            'lowest_average_separation_factor': np.inf,
            'highest_recovery': -np.inf,
            'lowest_recovery': np.inf,
            'highest_purity': -np.inf,
        }
    }

def update_data_to_pivot_table(data_to_pivot_table: dict, purity: float, recovery: float, separation_factor: float):
    data_to_pivot_table['approved']['highest_average_separation_factor'] = max(data_to_pivot_table['approved']['highest_average_separation_factor'], separation_factor)
    data_to_pivot_table['approved']['lowest_average_separation_factor'] = min(data_to_pivot_table['approved']['lowest_average_separation_factor'], separation_factor)
    data_to_pivot_table['approved']['highest_recovery'] = max(data_to_pivot_table['approved']['highest_recovery'], recovery)
    data_to_pivot_table['approved']['lowest_recovery'] = min(data_to_pivot_table['approved']['lowest_recovery'], recovery)
    data_to_pivot_table['approved']['highest_purity'] = max(data_to_pivot_table['approved']['highest_purity'], purity)

def store_condition(n_cells: int, ao_ratio: Number, pHi: Number, purity: Number, recovery: Number, separation_factor: Number) -> dict:
    return {
        'n_cells': n_cells,
        'ao_ratio': ao_ratio,
        'pHi': pHi,
        'purity': purity,
        'recovery': recovery,
        'separation_factor': separation_factor,
    }

def clear_result(rees: list[Ree], proton: Proton):
    for ree in rees:
        ree.cells_aq_concentrations = []
        ree.cells_org_concentrations = []
        ree.distribution_ratios = []

    proton.cells_concentrations = []
