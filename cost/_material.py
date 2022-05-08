from helpers._common import H_from_pH, g_in_ton, minutes_in_year, volume, area, Ka_from_pKa, current_extractant_concentration
from helpers._utils import value_or_default
from static_values._cost_assumptions import (HCL_MOLAR_CONCENTRATION,
                                             TOTAL_PRODUCTION)
from templates._types import Number

# ------------------ Phase Volumes

def calculate_phase_volumes(condition):
    total_aq_volume = g_in_ton(TOTAL_PRODUCTION) / condition['product_concentration_in_raffinate']
    total_org_volume = total_aq_volume / condition['ao_ratio']
    return total_aq_volume, total_org_volume

def calculate_org_phase_composition(total_org_volume, extractant) -> Number:
    # Inventory
    extractant_volume = total_org_volume / extractant['concentration'] / extractant['purity']
    solvent_volume = total_org_volume - extractant_volume
    return extractant_volume, solvent_volume

# ------------------ Flows

def calculate_flows(total_aq_volume: Number, total_org_volume: Number) -> Number:
    # Reference flow ensures that the fastest flow should still have a residence time great enough to meet equilibrium
    aq_flow_rate = total_aq_volume / minutes_in_year(1)
    org_flow_rate = total_org_volume / minutes_in_year(1)
    reference_flow = max(aq_flow_rate, org_flow_rate)
    return aq_flow_rate, org_flow_rate, reference_flow

# ------------------ Material Losses

def calculate_wasted_ree_until_permanent_state(mixer, settler, reference_flow, condition) -> Number:
    actual_mixing_time = value_or_default(mixer, 'VOLUME', volume(mixer['HEIGHT'], mixer['WIDTH'], mixer['DEPTH'])) / reference_flow
    actual_settling_time = value_or_default(settler, 'VOLUME', volume(settler['HEIGHT'], settler['WIDTH'], settler['DEPTH'])) / reference_flow
    time_until_permanent_state = (actual_mixing_time + actual_settling_time) * condition['n_cells']
    wasted_ree = condition['aq_feed_concentration'] * time_until_permanent_state
    return actual_settling_time, wasted_ree

def calculate_ree_loss(wasted_ree_until_permanent_state, total_aq_volume, condition) -> Number:
    loss_on_loaded_organic = condition['aq_feed_concentration'] * (1 - condition['recovery']) * total_aq_volume
    return loss_on_loaded_organic + wasted_ree_until_permanent_state

def calculate_extractant_loss(settling_time, settler, condition, extractant) -> Number:
    drag_loss = 0
    crude_loss = 0
    dissociation_loss = (Ka_from_pKa(extractant['pKa']) * H_from_pH(condition['raffinate_pH'])
                         / current_extractant_concentration(condition['ree'],
                                                            condition['n_cells'] - 1,
                                                            condition['ao_ratio'],
                                                            extractant['initial_concentration']))
    volatilization_loss = (area(settler['HEIGHT'], settler['WIDTH'])
                           * extractant['VOLATILIZATION_RATE']
                           * extractant['initial_concentration']
                           * settling_time)
    return drag_loss + crude_loss + dissociation_loss + volatilization_loss

def calculate_solvent_loss(settling_time, settler, solvent) -> Number:
    drag_loss = 0
    crude_loss = 0
    dissociation_loss = 0
    volatilization_loss = (area(settler['HEIGHT'], settler['WIDTH'])
                           * solvent['VOLATILIZATION_RATE']
                           * solvent['initial_concentration']
                           * settling_time)
    return drag_loss + crude_loss + dissociation_loss + volatilization_loss

def calculate_acid_loss(total_aq_volume, condition) -> Number:
    acid_volume_to_pHi = (total_aq_volume * H_from_pH(condition['pHi']) / HCL_MOLAR_CONCENTRATION)
    # TODO
    ree_concentration_to_strip = 0
    acid_to_stripping = 0
    return acid_volume_to_pHi + acid_to_stripping
