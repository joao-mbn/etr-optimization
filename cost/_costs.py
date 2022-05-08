from functools import reduce

from helpers._utils import default_if_none
from static_values._cost_assumptions import (ENERGY_COST_PER_KWH, FEED_LIQUOR,
                                             HCL_PRICE, ISOPARAFFIN,
                                             OPERATORS_COST)
from templates._types import Number

from cost._equipments import get_equipments
from cost._material import (calculate_acid_loss, calculate_extractant_loss,
                            calculate_flows, calculate_org_phase_composition,
                            calculate_phase_volumes, calculate_ree_loss,
                            calculate_solvent_loss,
                            calculate_wasted_ree_until_permanent_state)


def calculate_cost(condition, extractant, solvent = None) -> Number:

    # Annual Volumes Output (L/year)
    total_aq_volume, total_org_volume = calculate_phase_volumes(condition)
    extractant_volume, solvent_volume = calculate_org_phase_composition(total_org_volume, extractant)

    # Flow rates (L/min)
    aq_flow_rate, org_flow_rate, reference_flow = calculate_flows(total_aq_volume, total_org_volume)

    # Equipments
    equipments = get_equipments(aq_flow_rate, org_flow_rate, reference_flow)

    capital_cost = calculate_capital_cost(equipments,
                                          condition,
                                          extractant_volume,
                                          solvent_volume,
                                          extractant,
                                          default_if_none(solvent, ISOPARAFFIN))

    operating_cost = calculate_operating_cost(equipments['cell'],
                                              reference_flow,
                                              total_aq_volume,
                                              condition,
                                              extractant,
                                              default_if_none(solvent, ISOPARAFFIN))

    return capital_cost + operating_cost

def calculate_capital_cost(equipments, condition, extractant_volume, solvent_volume, extractant, solvent) -> Number:
    inventory_cost = solvent_volume * solvent['PRICE'] + extractant_volume * extractant['PRICE']

    equipments_cost = reduce(lambda x, y: x + y,
                             [value['PRICE'] * condition['n_cells'] if key in ('cell', 'agitator') else value['PRICE']
                              for key, value in equipments.items()])

    return inventory_cost + equipments_cost

def calculate_operating_cost(cell, reference_flow, total_aq_volume, condition, extractant, solvent) -> Number:

    settling_time, wasted_ree_until_permanent_state = calculate_wasted_ree_until_permanent_state(
        cell['MIXER'], cell['SETTLER'], reference_flow, condition)

    return (
        calculate_ree_loss(wasted_ree_until_permanent_state, total_aq_volume, condition) * FEED_LIQUOR['PRICE']
        + calculate_extractant_loss(settling_time, cell['SETTLER'], condition, extractant) * extractant['PRICE']
        + calculate_solvent_loss(settling_time, cell['SETTLER'], solvent) * solvent['PRICE']
        + calculate_acid_loss(total_aq_volume, condition) * HCL_PRICE
        + energy_cost() * ENERGY_COST_PER_KWH
        + OPERATORS_COST
    )

def energy_cost() -> Number:

    # TODO
    equipment_efficiency = 1 # efficiency of the pumps and agitators
    needed_energy = 0 # energy requirement for the pumps and agitators
    actual_consumed_energy = needed_energy * equipment_efficiency

    return actual_consumed_energy
