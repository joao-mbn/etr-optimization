from helpers._utils import value_or_default
from static_values._rees import REES
from static_values._substances import EXTRACTANTS, SOLVENTS

from templates._classes import Extractant, Ree, Solvent

"""
These factories are simply a handy way to instance full objects passing only a few properties, drawing the rest from the static values.
Useful for stuff with many physical-chemical properties, belonging to a more or less defined group.
"""

def rees_factory(wannabe_rees: list[dict]) -> list[Ree]:
    rees: list[Ree] = []
    for wannabe_ree in wannabe_rees:
        REE = next(filter(lambda REE: REE['SYMBOL'] == wannabe_ree['symbol'], REES))
        ree = ree_factory(REE, wannabe_ree)
        rees.append(ree)
    rees.sort(key = lambda ree: ree.atom_molar_mass)
    return rees

def ree_factory(REE: dict, wannabe_ree: dict) -> Ree:
    props = dict(
        aq_feed_concentration = wannabe_ree['aq_feed_concentration'],
        name = REE['NAME'],
        symbol = REE['SYMBOL'],
        atom_molar_mass = REE['ATOMIC_WEIGHT'],
        oxide_molar_mass = REE['OXIDE_WEIGHT'],
        valency = REE['VALENCY'],
        stoichiometric_proportion = REE['OXIDE_STOICHIOMETRIC_PROPORTION'],
        org_feed_concentration = value_or_default(wannabe_ree, 'org_feed_concentration', 0),
        model_coefficients = wannabe_ree['model_coefficients']
    )
    return Ree(**props)

def extractant_factory(wannabe_extractant: dict) -> Extractant:
    extractant = next(filter(lambda extractant: extractant['NAME'] == wannabe_extractant['name'], EXTRACTANTS))
    props = dict(
        name = extractant['NAME'],
        price = extractant['PRICE'],
        volumetric_concentration = wannabe_extractant['concentration'],
        molecular_weight = extractant['MOLECULAR_WEIGHT'],
        purity = extractant['PURITY'],
        density = extractant['DENSITY'],
        pKa = extractant['PKA'],
    )
    return Extractant(**props)

def solvent_factory(wannabe_solvent: dict) -> Solvent:
    solvent = next(filter(lambda solvent: solvent['NAME'] == wannabe_solvent['name'], SOLVENTS))
    props = dict(
        name = solvent['NAME'],
        price = solvent['PRICE'],
        volumetric_concentration = wannabe_solvent['concentration'],
        molecular_weight = solvent['MOLECULAR_WEIGHT'],
        purity = solvent['PURITY'],
        density = solvent['DENSITY'],
        solubility_in_water = solvent['SOLUBILITY_IN_WATER'],
    )
    return Solvent(**props)
