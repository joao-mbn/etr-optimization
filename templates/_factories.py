from static_values._rees import REES
from static_values._substances import EXTRACTANTS, SOLVENTS
from helpers._utils import value_or_default

from templates._classes import Ree, Extractant, Solvent


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
    EXTRACTANT = next(filter(lambda EXTRACTANT: EXTRACTANT['NAME'] == wannabe_extractant['name'], EXTRACTANTS))
    props = dict(
        name = EXTRACTANT['NAME'],
        price = EXTRACTANT['PRICE'],
        volumetric_concentration = wannabe_extractant['concentration'],
        molecular_weight = EXTRACTANT['MOLECULAR_WEIGHT'],
        purity = EXTRACTANT['PURITY'],
        density = EXTRACTANT['DENSITY'],
        volatilization_rate = EXTRACTANT['VOLATILIZATION_RATE'],
        pKa = EXTRACTANT['PKA'],
    )
    return Extractant(**props)

def solvent_factory(wannabe_solvent: dict) -> Solvent:
    SOLVENT = next(filter(lambda SOLVENT: SOLVENT['NAME'] == wannabe_solvent['name'], SOLVENTS))
    props = dict(
        name = SOLVENT['NAME'],
        price = SOLVENT['PRICE'],
        volumetric_concentration = wannabe_solvent['concentration'],
        molecular_weight = SOLVENT['MOLECULAR_WEIGHT'],
        purity = SOLVENT['PURITY'],
        density = SOLVENT['DENSITY'],
        volatilization_rate = SOLVENT['VOLATILIZATION_RATE'],
    )
    return Solvent(**props)