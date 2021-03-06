import math as m
from typing import TypeAlias

import numpy as np
import pandas as pd
from static_values._rees import SEPARATION_ORDER
from templates._classes import Ree
from templates._types import Number, Vector

from helpers._utils import has_any_substring, is_residue, value_or_default

Rees: TypeAlias = list[Ree]

# ----------------- Mass Conversions

def mass_from_mol(mol: Number, especies_weight: Number) -> Number: return mol * especies_weight
def mol_from_mass(mass: Number, especies_weight: Number) -> Number: return mass / especies_weight

def mol_atom_from_mol_oxide(mol_oxide: Number, stoichiometric_proportion: Number) -> Number: return mol_oxide * stoichiometric_proportion
def mol_oxide_from_mol_atom(mol_atom: Number, stoichiometric_proportion: Number) -> Number: return mol_atom / stoichiometric_proportion

def mol_atom_from_mass_oxide(mass_oxide: Number, stoichiometric_proportion: Number, oxide_weight: Number) -> Number:
    mol_oxide = mol_from_mass(mass_oxide, oxide_weight)
    mol_atom = mol_atom_from_mol_oxide(mol_oxide, stoichiometric_proportion)
    return mol_atom

def mass_oxide_from_mol_atom(mol_atom: Number, stoichiometric_proportion: Number, oxide_weight: Number) -> Number:
    mol_oxide = mol_oxide_from_mol_atom(mol_atom, stoichiometric_proportion)
    mass_oxide = mass_from_mol(mol_oxide, oxide_weight)
    return mass_oxide

# ----------------- Parameters Calculation

def pH_from_H(proton_concentration: Number) -> Number: return - m.log10(proton_concentration)
def H_from_pH(pH: Number) -> Number: return 10 ** -pH

def pKa_from_Ka(Ka: Number) -> Number: return - m.log10(Ka)
def Ka_from_pKa(pKa: Number) -> Number: return 10 ** -pKa


def org_concentrations(aq_concentrations: Vector, distribution_ratios: Vector) -> Vector:
    return np.multiply(aq_concentrations, distribution_ratios).tolist()


def area_of_rectangle(height: Number, width: Number) -> Number: return height * width

def area_of_circle(diameter: Number, radius: Number | None = None) -> Number:
    return m.pi * radius ** 2 if radius is not None else m.pi * diameter ** 2 / 4

def volume_of_parallelepiped(height: Number, width: Number, depth: Number) -> Number:
    return height * width * depth

def volume_of_mixer_settler(mixer, settler):
    mixer_volume = value_or_default(mixer, 'VOLUME',
                                    volume_of_parallelepiped(value_or_default(mixer, 'HEIGHT', 0),
                                                             value_or_default(mixer, 'WIDTH', 0),
                                                             value_or_default(mixer, 'DEPTH', 0)))
    settler_volume = value_or_default(settler, 'VOLUME',
                                      volume_of_parallelepiped(value_or_default(settler, 'HEIGHT', 0),
                                                               value_or_default(settler, 'WIDTH', 0),
                                                               value_or_default(settler, 'DEPTH', 0)))

    return mixer_volume, settler_volume

# ----------------- Indicators Calculation

def purity(products: Number, contaminants: Number) -> float:
    return 0 if products == 0 else products / (products + contaminants)

def recovery(initially: Number, lastly: Number) -> float: return lastly / initially

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


def create_sub_dataframe(df: pd.DataFrame, white_list_substrings: list[str] = [], black_list_substrings: list[str] = []) -> pd.DataFrame:
    columns_to_remain = [column for column in df.columns if is_column_of_interest(column, white_list_substrings, black_list_substrings)]
    return df[columns_to_remain]


def is_column_of_interest(column: str, white_list_substrings: list[str], black_list_substrings: list[str]) -> bool:
    has_white_listed_substring = has_any_substring(white_list_substrings, column)
    has_black_listed_substring = has_any_substring(black_list_substrings, column)

    return (has_white_listed_substring or len(white_list_substrings) == 0) and not has_black_listed_substring
