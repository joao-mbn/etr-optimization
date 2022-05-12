from functools import reduce

from static_values._miscellaneous import ENERGY_COST_PER_KWH, OPERATORS_COST
from static_values._substances import FEED_LIQUOR, HCL
from templates._classes import Extractant, Solvent
from templates._models import Condition
from templates._types import Number

from cost._energy import energy_consumption
from cost._equipments import get_equipments
from cost._material import (calculate_acid_loss, calculate_extractant_loss,
                            calculate_flows, calculate_org_phase_composition,
                            calculate_phase_volumes, calculate_ree_loss,
                            calculate_solvent_loss,
                            calculate_wasted_ree_until_permanent_state)


def calculate_cost(condition: Condition, extractant: Extractant, solvent: Solvent) -> Number:

    total_aq_volume, total_org_volume = calculate_phase_volumes(condition)
    extractant.volume, solvent.volume = calculate_org_phase_composition(total_org_volume, extractant)

    aq_flow_rate, org_flow_rate, reference_flow = calculate_flows(total_aq_volume, total_org_volume)

    equipments, operating_powers, total_pipe_length = get_equipments(aq_flow_rate, org_flow_rate, reference_flow,
                                                                     extractant, solvent, condition)

    capital_cost = calculate_capital_cost(equipments, total_pipe_length, condition.n_cells, extractant, solvent)
    operating_cost = calculate_operating_cost(equipments['cell'], reference_flow, total_aq_volume, total_org_volume,
                                              condition, extractant, solvent, operating_powers)

    return capital_cost + operating_cost

def calculate_capital_cost(equipments, total_pipe_length: Number, n_cells: int, extractant: Extractant, solvent: Solvent) -> Number:

    inventory_cost = reduce(lambda x, y: x + y,
                            [calculate_and_conform_pounderal_price(x.volume, x.price, x.density) for x in (extractant, solvent)])

    equipments_cost = reduce(lambda x, y: x + y,
                             [equipment['PRICE'] * n_cells if key in ('cell', 'agitator')
                              else equipment['PRICE_PER_LENGTH'] * total_pipe_length if key in ('pipe')
                              else equipment['PRICE']
                              for key, equipment in equipments.items()])

    return inventory_cost + equipments_cost

def calculate_operating_cost(cell, reference_flow: Number, total_aq_volume: Number, total_org_volume: Number,
                             condition: Condition, extractant: Extractant, solvent: Solvent, operating_powers: dict[str, Number]) -> Number:

    settling_time, wasted_ree_until_permanent_state = calculate_wasted_ree_until_permanent_state(
        cell['MIXER'], cell['SETTLER'], reference_flow, condition)

    volume_of_lost_acid = calculate_acid_loss(total_aq_volume, total_org_volume, condition.pHi)
    volume_of_lost_extractant = calculate_extractant_loss(settling_time, cell['SETTLER'], total_org_volume, condition, extractant)
    volume_of_lost_solvent = calculate_solvent_loss(settling_time, cell['SETTLER'], total_org_volume, solvent)

    ree_loss = calculate_ree_loss(wasted_ree_until_permanent_state, total_aq_volume, condition) * FEED_LIQUOR['PRICE']
    energy_loss = energy_consumption(condition.n_cells, **operating_powers) * ENERGY_COST_PER_KWH
    acid_loss = calculate_and_conform_pounderal_price(volume_of_lost_acid, HCL['PRICE'], HCL['DENSITY'])
    extractant_loss = calculate_and_conform_pounderal_price(volume_of_lost_extractant, extractant.price, extractant.density)
    solvent_loss = calculate_and_conform_pounderal_price(volume_of_lost_solvent, solvent.price, solvent.density)

    return ree_loss + extractant_loss + solvent_loss + acid_loss + energy_loss + OPERATORS_COST

def calculate_and_conform_pounderal_price(volume, price, density):
    return volume * price if price.check('[currency]/[volume]') else volume * density * price