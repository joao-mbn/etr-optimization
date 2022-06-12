from functools import reduce

from static_values._miscellaneous import (ENERGY_COST,
                                          INTEREST_RATE_ON_CAPITAL,
                                          MARGIN_OF_SAFETY,
                                          NUMBER_OF_CELLS_IN_STRIPPING_SECTION,
                                          NUMBER_OF_OPERATORS_PER_POSITION,
                                          NUMBER_OF_POSITIONS, OPERATOR_COST,
                                          TIME_REFERENCE)
from static_values._substances import HCL
from templates._classes import Extractant, Solvent
from templates._models import Condition, Project
from templates._types import Number, Scalar
from templates._units import unit_registry as ur

from cost._energy import calculate_energy_consumption
from cost._equipments import get_equipments
from cost._material import (calculate_acid_loss, calculate_extractant_loss,
                            calculate_flows, calculate_org_phase_composition,
                            calculate_ree_loss, calculate_solvent_loss,
                            calculate_total_aqueous_volume,
                            calculate_total_organic_volume,
                            calculate_wasted_ree_until_permanent_state)


def calculate_cost(condition: Condition, project: Project) -> Number:

    costs: dict[str, Scalar] = {}

    extractant, solvent, mineral, reos_of_interest_mineral_content = project.extractant, project.solvent, project.mineral, project.reos_of_interest_mineral_content

    total_aq_volume = calculate_total_aqueous_volume(condition)
    aq_flow_rate, org_flow_rate, reference_flow, total_flow_rate = calculate_flows(condition)

    equipments, operating_powers, total_pipe_length = get_equipments(aq_flow_rate, org_flow_rate, reference_flow,
                                                                     total_flow_rate, extractant, solvent, condition)

    total_org_volume = calculate_total_organic_volume(equipments['cell'], condition.ao_ratio, condition.n_cells)
    extractant.volume, solvent.volume = calculate_org_phase_composition(total_org_volume, extractant)

    calculate_interest_on_capital(equipments, total_pipe_length, condition.n_cells, extractant, solvent, costs)
    calculate_operating_cost(equipments['cell'], reference_flow, aq_flow_rate, total_aq_volume, total_org_volume, condition,
                             extractant, solvent, operating_powers, mineral, reos_of_interest_mineral_content, costs)

    costs['raw total cost'] = costs['interest on capital'] + costs['operating cost']
    costs['total cost'] = costs['raw total cost'] * MARGIN_OF_SAFETY

    costs.update((key, value.to('usd')) for key, value in costs.items())

    return costs


def calculate_interest_on_capital(equipments, total_pipe_length: Number, n_cells: int, extractant: Extractant,
                                  solvent: Solvent, costs: dict[str, Scalar]) -> None:

    inventory_cost = reduce(lambda x, y: x + y,
                            [calculate_and_conform_pounderal_price(x.volume, x.price, x.density) for x in (extractant, solvent)])

    equipments_cost = reduce(lambda x, y: x + y,
                             [equipment['PRICE'] * (n_cells + NUMBER_OF_CELLS_IN_STRIPPING_SECTION) if key in ('cell')
                              else equipment['PRICE_PER_LENGTH'] * total_pipe_length if key in ('pipe')
                              else equipment['PRICE']
                              for key, equipment in equipments.items()])

    costs['interest on inventory'] = inventory_cost * TIME_REFERENCE * INTEREST_RATE_ON_CAPITAL
    costs['interest on equipments'] = equipments_cost * TIME_REFERENCE * INTEREST_RATE_ON_CAPITAL

    costs['interest on capital'] = costs['interest on inventory'] + costs['interest on equipments']


def calculate_operating_cost(cell, reference_flow: Number, aq_flow_rate: Number, total_aq_volume: Number, total_org_volume: Number,
                             condition: Condition, extractant: Extractant, solvent: Solvent,
                             operating_powers: dict[str, Number], mineral: dict[str, str | Scalar],
                             reos_of_interest_mineral_content: float, costs: dict[str, Scalar]) -> None:

    settling_time, wasted_ree_until_permanent_state = calculate_wasted_ree_until_permanent_state(
        cell['MIXER'], cell['SETTLER'], reference_flow, aq_flow_rate, condition)

    volume_of_lost_acid, volume_of_stripping_section = calculate_acid_loss(total_aq_volume, condition.ao_ratio, condition.pHi)
    volume_of_lost_extractant = calculate_extractant_loss(settling_time, cell['SETTLER'], total_aq_volume, condition, extractant, volume_of_stripping_section)
    volume_of_lost_solvent = calculate_solvent_loss(total_aq_volume, solvent, volume_of_stripping_section)

    ree_loss = calculate_ree_loss(wasted_ree_until_permanent_state, total_aq_volume, condition) * mineral['PRICE'] / mineral['REO_CONTENT'] / reos_of_interest_mineral_content
    acid_loss = calculate_and_conform_pounderal_price(volume_of_lost_acid, HCL['PRICE'], HCL['DENSITY'])
    extractant_loss = calculate_and_conform_pounderal_price(volume_of_lost_extractant, extractant.price, extractant.density)
    solvent_loss = calculate_and_conform_pounderal_price(volume_of_lost_solvent, solvent.price, solvent.density)

    energy_loss = calculate_energy_consumption(condition.n_cells, **operating_powers) * ENERGY_COST

    operators_cost = OPERATOR_COST * NUMBER_OF_OPERATORS_PER_POSITION * NUMBER_OF_POSITIONS * TIME_REFERENCE

    costs['ree loss'] = ree_loss
    costs['acid loss'] = acid_loss
    costs['extractant loss'] = extractant_loss
    costs['solvent loss'] = solvent_loss
    costs['energy loss'] = energy_loss
    costs['operators cost'] = operators_cost

    costs['operating cost'] = (ree_loss + acid_loss + extractant_loss + solvent_loss + energy_loss + operators_cost)


@ur.wraps(('usd'), (None, None, None))
def calculate_and_conform_pounderal_price(volume, price, density):
    return volume * price if price.check('[currency]/[volume]') else volume * density * price
