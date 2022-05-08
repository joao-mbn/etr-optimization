from typing import Any
from helpers._common import H_from_pH, g_in_ton, minutes_in_year, volume
from helpers._utils import value_or_default
from static_values._cost_assumptions import (HCL_MOLAR_CONCENTRATION,
                                             PHASE_SETTLING_TIME,
                                             REE_SX_EQUILIBRIUM_TIME,
                                             TOTAL_PRODUCTION,
                                             MIXER_SETTLERS)
from templates._types import Number

def preliminary_calculations(condition, extractant):

    # Note: Note all keys actually exist in the condition dictionary

    # Annual Volumes Output (L/year)
    total_aq_volume, total_org_volume = calculate_phase_volumes(condition)
    extractant_volume, solvent_volume = calculate_org_phase_composition(total_org_volume, extractant)

    # Flow rates (L/min)
    aq_flow_rate, org_flow_rate, reference_flow = calculate_flows(total_aq_volume, total_org_volume)

    # Equipments
    cell = get_adequate_cell(reference_flow)
    settling_time, wasted_ree_until_permanent_state = calculate_wasted_ree_until_permanent_state(
        cell['MIXER'], cell['SETTLER'], reference_flow, condition)


    # TODO ZONE

    agitator = get_adequate_agitator()
    aq_pump = get_adequate_pump(aq_flow_rate)
    org_pump = get_adequate_pump(org_flow_rate)

    equipment_efficiency = 1 # efficiency of the pumps and agitators
    needed_energy = 0 # energy requirement for the pumps and agitators
    actual_consumed_energy = needed_energy * equipment_efficiency

    ree_concentration_to_strip = 0
    acid_consumption = calculate_acid_consumption(total_aq_volume, condition, ree_concentration_to_strip)

    return dict(
        total_aq_volume=total_aq_volume,
        total_org_volume=total_org_volume,
        solvent_volume=solvent_volume,
        extractant_volume=extractant_volume,
        acid_consumption=acid_consumption,
        actual_consumed_energy=actual_consumed_energy,
        cell=cell,
        agitator = agitator,
        aq_pump = aq_pump,
        org_pump = org_pump,
        wasted_ree_until_permanent_state=wasted_ree_until_permanent_state,
        settling_time=settling_time,
    )

# ------------------------------------ Phase and Flows

def calculate_phase_volumes(condition):
    total_aq_volume = g_in_ton(TOTAL_PRODUCTION) / condition['product_concentration_in_raffinate']
    total_org_volume = total_aq_volume / condition['ao_ratio']
    return total_aq_volume, total_org_volume

def calculate_org_phase_composition(total_org_volume, extractant) -> Number:
    # Inventory
    extractant_volume = total_org_volume / extractant['concentration'] / extractant['purity']
    solvent_volume = total_org_volume - extractant_volume
    return extractant_volume, solvent_volume

def calculate_acid_consumption(total_aq_volume, condition, ree_concentration_to_strip) -> Number:
    acid_volume_to_pHi = (total_aq_volume * H_from_pH(condition['pHi']) / HCL_MOLAR_CONCENTRATION)
    acid_to_stripping = 0
    return acid_volume_to_pHi + acid_to_stripping

def calculate_flows(total_aq_volume: Number, total_org_volume: Number) -> Number:
    # Reference flow ensures that the fastest flow should still have a residence time great enough to meet equilibrium
    aq_flow_rate = total_aq_volume / minutes_in_year(1)
    org_flow_rate = total_org_volume / minutes_in_year(1)
    reference_flow = max(aq_flow_rate, org_flow_rate)
    return aq_flow_rate, org_flow_rate, reference_flow

def calculate_wasted_ree_until_permanent_state(mixer, settler, reference_flow, condition) -> Number:
    actual_mixing_time = value_or_default(mixer, 'VOLUME', volume(mixer['HEIGHT'], mixer['WIDTH'], mixer['DEPTH'])) / reference_flow
    actual_settling_time = value_or_default(settler, 'VOLUME', volume(settler['HEIGHT'], settler['WIDTH'], settler['DEPTH'])) / reference_flow
    time_until_permanent_state = (actual_mixing_time + actual_settling_time) * condition['n_cells']
    wasted_ree = condition['aq_feed_concentration'] * time_until_permanent_state
    return actual_settling_time, wasted_ree

# ------------------------------------ Equipments

def get_adequate_cell(reference_flow: Number):
    smallest_mixer_possible = reference_flow * REE_SX_EQUILIBRIUM_TIME # Volume in L
    smallest_settler_possible = reference_flow * PHASE_SETTLING_TIME   # Volume in L
    big_enough_cells: list[Any] = []

    for cell in MIXER_SETTLERS:
        mixer, settler = cell['MIXER'], cell['SETTLER']
        mixer_volume = value_or_default(mixer, 'VOLUME', volume(mixer['HEIGHT'], mixer['WIDTH'], mixer['DEPTH']))
        settler_volume = value_or_default(settler, 'VOLUME', volume(settler['HEIGHT'], settler['WIDTH'], settler['DEPTH']))
        if mixer_volume >= smallest_mixer_possible and settler_volume >= smallest_settler_possible:
            big_enough_cells.append(cell)

    big_enough_cells.sort(key=lambda cell: cell['PRICE'])
    return big_enough_cells[0]

def get_adequate_pump(flow_rate: Number) -> Number:
    pass

def get_adequate_agitator():
    pass