from helpers._common import (H_from_pH, Ka_from_pKa, area,
                             current_extractant_concentration, g_in_ton,
                             minutes_in_year, volume)
from helpers._utils import default_if_none
from static_values._cost_assumptions import (ENERGY_COST_PER_KWH, FEED_LIQUOR,
                                             HCL_MOLAR_CONCENTRATION,
                                             ISOPARAFFIN, OPERATORS_COST,
                                             PHASE_SETTLING_TIME,
                                             REE_SX_EQUILIBRIUM_TIME,
                                             TOTAL_PRODUCTION)
from templates._types import Number

from cost._preliminary_calculations import preliminary_calculations


def calculate_cost(condition, extractant, solvent = None) -> Number:

    data = preliminary_calculations(condition, extractant)

    return capital_cost() + operating_cost(data, condition, extractant, default_if_none(solvent, ISOPARAFFIN))

def capital_cost() -> Number:
    pass

def operating_cost(data, condition, extractant, solvent) -> Number:
    return (
        calculate_ree_loss(data, condition)
        + calculate_extractant_loss(data, condition, extractant)
        + calculate_solvent_loss(data, condition, solvent)
        + energy_cost(data['actual_consumed_energy'])
        + OPERATORS_COST
    )

def calculate_ree_loss(data, condition) -> Number:
    loss_on_loaded_organic = condition['aq_feed_concentration'] * (1 - condition['recovery']) * data['total_aq_volume']
    return (loss_on_loaded_organic + data['wasted_ree_until_permanent_state']) * FEED_LIQUOR['PRICE']

def calculate_extractant_loss(data, condition, extractant) -> Number:
    drag_loss = 0
    crude_loss = 0
    dissociation_loss = (Ka_from_pKa(extractant['pKa'])
                         * H_from_pH(condition['raffinate_pH'])
                         / current_extractant_concentration(condition['ree'], condition['n_cells'] - 1, extractant['initial_concentration']))
    settler = data['cell']['SETTLER']
    volatilization_loss = (area(settler['HEIGHT'], settler['WIDTH'])
                           * extractant['VOLATILIZATION_RATE']
                           * extractant['initial_concentration']
                           * data['settling_time'])
    return (drag_loss + crude_loss + dissociation_loss + volatilization_loss) * extractant['PRICE']

def calculate_solvent_loss(data, condition, solvent) -> Number:
    drag_loss = 0
    crude_loss = 0
    dissociation_loss = 0
    settler = data['cell']['SETTLER']
    volatilization_loss = (area(settler['HEIGHT'], settler['WIDTH'])
                           * solvent['VOLATILIZATION_RATE']
                           * solvent['initial_concentration']
                           * data['settling_time'])
    return (drag_loss + crude_loss + dissociation_loss + volatilization_loss) * solvent['PRICE']

def energy_cost(energy_consumption) -> Number:
    return ENERGY_COST_PER_KWH * energy_consumption
