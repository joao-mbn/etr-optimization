from helpers._common import (H_from_pH, Ka_from_pKa, area_of_rectangle,
                             free_extractant_on_last_cell, g_in_ton,
                             minutes_in_year, volume_of_parallelepiped)
from helpers._utils import value_or_default
from static_values._miscellaneous import (
    STRIPPING_SOLUTION_ACID_CONCENTRATION, TOTAL_PRODUCTION)
from static_values._substances import HCL
from templates._types import Number
from templates._classes import Extractant, Solvent
from templates._models import Condition

# ------------------ Phase Volumes

def calculate_phase_volumes(condition: Condition):
    total_aq_volume = g_in_ton(TOTAL_PRODUCTION) / condition.product_at_raffinate
    total_org_volume = total_aq_volume / condition.ao_ratio
    return total_aq_volume, total_org_volume

def calculate_org_phase_composition(total_org_volume: Number, extractant: Extractant) -> tuple[Number, Number]:
    extractant_volume = total_org_volume / extractant.volumetric_concentration / extractant.purity
    solvent_volume = total_org_volume - extractant_volume
    return extractant_volume, solvent_volume

# ------------------ Flows

def calculate_flows(total_aq_volume: Number, total_org_volume: Number) -> tuple[Number, Number, Number]:
    # Reference flow ensures that the fastest flow should still have a residence time great enough to meet equilibrium
    aq_flow_rate = total_aq_volume / minutes_in_year(1)
    org_flow_rate = total_org_volume / minutes_in_year(1)
    reference_flow = max(aq_flow_rate, org_flow_rate)
    return aq_flow_rate, org_flow_rate, reference_flow

# ------------------ Material Losses

def calculate_wasted_ree_until_permanent_state(mixer, settler, reference_flow, condition) ->  tuple[Number, Number]:
    actual_mixing_time = value_or_default(mixer, 'VOLUME', volume_of_parallelepiped(mixer['HEIGHT'], mixer['WIDTH'], mixer['DEPTH'])) / reference_flow
    actual_settling_time = value_or_default(settler, 'VOLUME', volume_of_parallelepiped(settler['HEIGHT'], settler['WIDTH'], settler['DEPTH'])) / reference_flow
    time_until_permanent_state = (actual_mixing_time + actual_settling_time) * condition.n_cells
    wasted_ree = condition.product_at_feed * time_until_permanent_state
    return actual_settling_time, wasted_ree

def calculate_ree_loss(wasted_ree_until_permanent_state: Number, total_aq_volume: Number, condition: Condition) -> Number:
    loss_on_loaded_organic = condition.product_at_feed * (1 - condition.recovery) * total_aq_volume
    return loss_on_loaded_organic + wasted_ree_until_permanent_state

def calculate_extractant_loss(settling_time: Number, settler, condition: Condition, extractant: Extractant) -> Number:
    drag_loss = 0
    crude_loss = 0
    dissociation_loss = (Ka_from_pKa(extractant.pKa) * H_from_pH(condition.pH_at_raffinate)
                         / free_extractant_on_last_cell(condition.product_at_feed,
                                                        condition.product_at_raffinate,
                                                        condition.ao_ratio,
                                                        extractant.molar_concentration))
    volatilization_loss = (area_of_rectangle(settler['HEIGHT'], settler['WIDTH'])
                           * extractant.volatilization_rate
                           * extractant.volumetric_concentration
                           * settling_time)
    return drag_loss + crude_loss + dissociation_loss + volatilization_loss

def calculate_solvent_loss(settling_time: Number, settler, solvent: Solvent) -> Number:
    drag_loss = 0
    crude_loss = 0
    dissociation_loss = 0
    volatilization_loss = (area_of_rectangle(settler['HEIGHT'], settler['WIDTH'])
                           * solvent.volatilization_rate
                           * solvent.volumetric_concentration
                           * settling_time)
    return drag_loss + crude_loss + dissociation_loss + volatilization_loss

def calculate_acid_loss(total_aq_volume: Number, total_org_volume: Number, pHi: Number) -> Number:
    """
    The stripping occurs with ao_ratio = 1 between stripping solution and organic phase.
    It is assumed that the stripping solution is enough to clear organic phase from REEs.
    """
    acid_to_pHi = (total_aq_volume * H_from_pH(pHi) / HCL['MOLAR_CONCENTRATION'])
    acid_to_stripping = total_org_volume * STRIPPING_SOLUTION_ACID_CONCENTRATION / HCL['MOLAR_CONCENTRATION']
    return acid_to_pHi + acid_to_stripping
