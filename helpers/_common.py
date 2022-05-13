import math as m
from typing import Any, TypeAlias

import numpy as np
from pandas import DataFrame
from pint import Quantity
from static_values._rees import SEPARATION_ORDER
from templates._classes import Ree
from templates._models import Condition
from templates._types import Number, Vector

from helpers._utils import is_residue

Rees: TypeAlias = list[Ree]

# ----------------- Mass Conversions

def g_from_mol(mol: Number, molecular_weight: Number) -> Number:
    return mol * molecular_weight

def mol_from_g(g: Number, molecular_weight: Number) -> Number:
    return g / molecular_weight

def oxide_from_atom(atom_concentration: Number, stoichiometric_proportion: Number, atomic_weight: Number, oxide_weight: Number) -> Number:
    """stoichiometric_proportion is the number of that atom in the oxide. e.g. Nd -> Nd2O3 = 2. Pr -> Pr6O11 = 6."""
    return atom_concentration * stoichiometric_proportion * oxide_weight / atomic_weight

def atom_from_oxide(oxide_concentration: Number, stoichiometric_proportion: Number, atomic_weight: Number, oxide_weight: Number) -> Number:
    """stoichiometric_proportion is the number of that atom in the oxide. e.g. Nd -> Nd2O3 = 2. Pr -> Pr6O11 = 6."""
    return oxide_concentration * atomic_weight / oxide_weight / stoichiometric_proportion

# ----------------- Parameters Calculation

def pH_from_H(proton_concentration: Number) -> Number:
    return - m.log10(proton_concentration)

def H_from_pH(pH: Number) -> Number:
    return 10 ** -pH

def pKa_from_Ka(Ka: Number) -> Number:
    return - m.log10(Ka)

def Ka_from_pKa(pKa: Number) -> Number:
    return 10 ** -pKa

def org_concentrations(aq_concentrations: Vector, distribution_ratios: Vector) -> Vector:
    return np.multiply(aq_concentrations, distribution_ratios).tolist()

def area_of_rectangle(height: Number, width: Number) -> Number:
    return height * width

def area_of_circle(diameter: Number, radius: Number | None = None) -> Number:
    return m.pi * radius ** 2 if radius is not None else m.pi * diameter ** 2 / 4

def volume_of_parallelepiped(height: Number, width: Number, depth: Number) -> Number:
    return height * width * depth

# ----------------- Indicators Calculation

def purity(products: Number, contaminants: Number) -> float:
    return 0 if products == 0 else products / (products + contaminants)

def recovery(initially: Number, lastly: Number) -> float:
    return lastly / initially

def separation_factor(distribution_ratio_of_lighter: Number, distribution_ratio_of_heavier: Number) -> float:
    return distribution_ratio_of_heavier / distribution_ratio_of_lighter

def are_results_absurd(rees: Rees) -> bool:
    return any(
        not is_residue(ree.cells_aq_concentrations[-1], ree.aq_feed_concentration) and
        ree.cells_aq_concentrations[-1] < 0 or
        ree.cells_aq_concentrations[-1] > ree.aq_feed_concentration
        for ree in rees)

def are_all_residues(rees: Rees) -> bool:
    return all(is_residue(ree.cells_aq_concentrations[-1], ree.aq_feed_concentration) for ree in rees)

# ----------------- Data Manipulation

def resolve_cut(cut: str):
    heavier = cut.split('/')[1]
    heavier_index = SEPARATION_ORDER.index(heavier)
    lighter_fraction = SEPARATION_ORDER[:heavier_index]
    heavier_fraction = SEPARATION_ORDER[heavier_index:]
    return lighter_fraction, heavier_fraction

def classify_rees(rees: Rees, lighter_fraction: list[str], heavier_fraction: list[str]) -> tuple[Rees, Rees]:
    lighter_cut = [ree for ree in rees if ree.symbol in lighter_fraction]
    heavier_cut = [ree for ree in rees if ree.symbol in heavier_fraction]
    return lighter_cut, heavier_cut

def transform_conditions_to_dataframe(conditions: list[Condition]) -> DataFrame:
    """
    Turns a list of conditions into a dictionary of its properties and than into a dataframe.
    Removes the units from individual cells and set it to the column.
    """
    data = [condition.__dict__ for condition in conditions]
    unitted_columns_names = add_units_to_columns(data[0])
    remove_units_from_data(data)
    df = DataFrame(data)
    df.rename(columns=unitted_columns_names, inplace=True)
    return df

def add_units_to_columns(data: dict[str, Any]) -> dict[str, str]:
    columns_to_update = dict()
    for key, value in data.items():
        if isinstance(value, Quantity):
            unit = f'({value.units})'.replace(' ', '') if not value.units.dimensionless else ''
        else:
            unit = ''
        columns_to_update[key] = f'{key} {unit}'.replace('_', ' ')
    return columns_to_update

def remove_units_from_data(data: list[dict[str, Any]]) -> None:
    for row in data:
        for key, value in row.items():
            if isinstance(value, Quantity):
                row[key] = value.magnitude
