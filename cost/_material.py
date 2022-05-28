from helpers._common import (H_from_pH, Ka_from_pKa, area_of_rectangle,
                             volume_of_parallelepiped)
from helpers._utils import value_or_default
from static_values._miscellaneous import (
    STRIPPING_SOLUTION_ACID_CONCENTRATION, TIME_REFERENCE, TOTAL_PRODUCTION)
from static_values._rees import REE_EXTRACTANT_STOICHIOMETRIC_PROPORTION
from static_values._substances import HCL
from templates._classes import Extractant, Solvent
from templates._models import Condition
from templates._types import Number, Scalar
from templates._units import quantity as Q
from templates._units import unit_registry as ur

# ------------------ Phase Volumes

@ur.wraps(('L'), (None))
def calculate_total_aqueous_volume(condition: Condition) -> Scalar:
    total_aq_volume = TOTAL_PRODUCTION / condition.mass_of_reo_product_at_raffinate
    return total_aq_volume

@ur.wraps(('L'), (None, None, None))
def calculate_total_organic_volume(cell, ao_ratio: Scalar, n_cells: int) -> Scalar:
    mixer, settler = cell['MIXER'], cell['SETTLER']
    mixer_volume = value_or_default(mixer, 'VOLUME', volume_of_parallelepiped(mixer['HEIGHT'], mixer['WIDTH'], mixer['DEPTH']))
    settler_volume = value_or_default(settler, 'VOLUME', volume_of_parallelepiped(settler['HEIGHT'], settler['WIDTH'], settler['DEPTH']))
    total_org_volume = (mixer_volume + settler_volume) * n_cells / ao_ratio
    return total_org_volume

@ur.wraps(('L', 'L'), (None, None))
def calculate_org_phase_composition(total_org_volume: Scalar, extractant: Extractant) -> tuple[Scalar, Scalar]:
    extractant_volume = total_org_volume * extractant.volumetric_concentration / extractant.purity
    solvent_volume = total_org_volume - extractant_volume
    return extractant_volume, solvent_volume

# ------------------ Flows

@ur.wraps(('L/min', 'L/min', 'L/min', 'L/min'), (None, None))
def calculate_flows(total_aq_volume: Scalar, ao_ratio: Scalar) -> tuple[Scalar, Scalar, Scalar, Scalar]:
    """
    Reference flow ensures that the fastest flow should still
    have a residence time great enough to meet equilibrium.
    """
    aq_flow_rate = total_aq_volume / TIME_REFERENCE
    org_flow_rate = aq_flow_rate / ao_ratio
    reference_flow = max(aq_flow_rate, org_flow_rate)
    total_flow_rate = aq_flow_rate + org_flow_rate
    return aq_flow_rate, org_flow_rate, reference_flow, total_flow_rate

# ------------------ Material Losses

@ur.wraps(('min', 'kg'), (None, None, None, None))
def calculate_wasted_ree_until_permanent_state(mixer, settler, reference_flow, condition: Condition) ->  tuple[Number, Number]:
    """
    It assumes that both ree in the raffinate and organic will be lost until permanent state.
    """
    actual_mixing_time = value_or_default(mixer, 'VOLUME', volume_of_parallelepiped(mixer['HEIGHT'], mixer['WIDTH'], mixer['DEPTH'])) / reference_flow
    actual_settling_time = value_or_default(settler, 'VOLUME', volume_of_parallelepiped(settler['HEIGHT'], settler['WIDTH'], settler['DEPTH'])) / reference_flow
    time_until_permanent_state = (actual_mixing_time + actual_settling_time) * condition.n_cells
    wasted_ree = condition.mass_of_reo_product_at_feed * time_until_permanent_state * reference_flow
    return actual_settling_time, wasted_ree

@ur.wraps(('kg'), (None, None, None))
def calculate_ree_loss(wasted_ree_until_permanent_state: Number, total_aq_volume: Number, condition: Condition) -> Number:
    """
    It assumes that all ree in the loaded organic will be lost.
    """
    loss_on_loaded_organic = condition.mass_of_reo_product_at_feed * total_aq_volume * (1 - condition.recovery)
    return loss_on_loaded_organic + wasted_ree_until_permanent_state

@ur.wraps(('L'), (None, None, None, None, None))
def calculate_extractant_loss(settling_time: Number, settler, total_org_volume: Number,
                              condition: Condition, extractant: Extractant) -> Number:
    """
    - No method for estimation of drag loss and crude loss are yet implemented.
    - It assumes that only the free ion of the extractant is capable of migrating to aqueous phase.
    - It assumes that acid-base equilibrium is the only equilibrium that would lead to formation of the extractant free ion.
    - It assumes that acid-base equilibrium of the extractant is instantaneous.
    """
    drag_loss = Q('0 kg')
    crude_loss = Q('0 kg')
    volatilization_loss = Q('0 kg')

    free_extractant_on_last_cell = (extractant.molar_concentration
                                    - REE_EXTRACTANT_STOICHIOMETRIC_PROPORTION
                                    * condition.ao_ratio
                                    * (condition.moles_of_ree_product_at_feed - condition.moles_of_ree_product_at_raffinate))

    ionized_extractants = Ka_from_pKa(extractant.pKa) * free_extractant_on_last_cell / H_from_pH(condition.pH_at_raffinate)
    dissociation_loss = ionized_extractants * total_org_volume * extractant.molecular_weight

    # - It assumes that volatilization occurs only at the settler, not at the tanks nor the mixer nor anywhere else.
    """ volatilization_loss = (area_of_rectangle(settler['HEIGHT'], settler['WIDTH'])
                           * extractant.volatilization_rate
                           * extractant.volumetric_concentration
                           * settling_time) """

    return (drag_loss + crude_loss + dissociation_loss + volatilization_loss) / extractant.density

@ur.wraps(('L'), (None, None))
def calculate_solvent_loss(total_aq_volume: Number, solvent: Solvent) -> Number:
    """
    - No method for estimation of drag loss, crude loss and volatilization loss are yet implemented.
    """
    drag_loss = Q('0 kg')
    crude_loss = Q('0 kg')
    dissociation_loss = Q('0 kg')
    volatilization_loss = solvent.solubility_in_water * total_aq_volume

    return (drag_loss + crude_loss + dissociation_loss + volatilization_loss) / solvent.density

@ur.wraps(('L'), (None, None, None))
def calculate_acid_loss(total_aq_volume: Number, total_org_volume: Number, pHi: Number) -> Number:
    """
    It assumes that the stripping occurs with A/O ratio 1, between stripping solution and organic phase.
    It assumes that the stripping solution is enough to clear organic phase from REEs.
    It assumes that the acid and the rees are herewith lost.
    """
    acid_to_pHi = (total_aq_volume * Q(H_from_pH(pHi), 'mol/L') / HCL['MOLAR_CONCENTRATION'])
    acid_to_stripping = total_org_volume * STRIPPING_SOLUTION_ACID_CONCENTRATION / HCL['MOLAR_CONCENTRATION']
    return acid_to_pHi + acid_to_stripping
