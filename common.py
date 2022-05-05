from _types import Number, Vector
import math as m
import numpy as np

def pH_from_H(proton_concentration: Number) -> Number:
    return - m.log10(proton_concentration)

def H_from_pH(pH: Number) -> Number:
    return 10 ** -pH

def g_from_mol(mol: Number, molecular_weight: Number) -> Number:
    return mol * molecular_weight

def mol_from_g(g: Number, molecular_weight: Number) -> Number:
    return g / molecular_weight

def oxide_from_atom(atom: Number, stoichiometric_proportion: Number, atomic_weight: Number, oxide_weight: Number) -> Number:
    """stoichiometric_proportion is the number of that atom in the oxide. e.g. Nd -> Nd2O3 = 2. Pr -> Pr6O11 = 6."""
    return atom * stoichiometric_proportion * oxide_weight / atomic_weight

def atom_from_oxide(oxide: Number, stoichiometric_proportion: Number, atomic_weight: Number, oxide_weight: Number) -> Number:
    """stoichiometric_proportion is the number of that atom in the oxide. e.g. Nd -> Nd2O3 = 2. Pr -> Pr6O11 = 6."""
    return oxide * atomic_weight / oxide_weight / stoichiometric_proportion

def org_concentrations(aq_concentrations: Vector, distribution_ratios: Vector) -> Vector:
    return np.multiply(aq_concentrations, distribution_ratios).tolist()