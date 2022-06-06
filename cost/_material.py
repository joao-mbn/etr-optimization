from helpers._common import H_from_pH, Ka_from_pKa, volume_of_mixer_settler
from static_values._miscellaneous import (
    AO_RATIO_IN_STRIPPING_SECTION, NUMBER_OF_CELLS_IN_STRIPPING_SECTION,
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
    mixer_volume, settler_volume = volume_of_mixer_settler(mixer, settler)
    total_org_volume = (mixer_volume + settler_volume) * (n_cells / ao_ratio + NUMBER_OF_CELLS_IN_STRIPPING_SECTION / AO_RATIO_IN_STRIPPING_SECTION)
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

@ur.wraps(('min', 'kg'), (None, None, None, None, None))
def calculate_wasted_ree_until_permanent_state(mixer, settler, reference_flow, aq_flow_rate, condition: Condition) ->  tuple[Number, Number]:
    """
    It assumes that both ree in the raffinate and organic will be lost until permanent state.
    """
    mixer_volume, settler_volume = volume_of_mixer_settler(mixer, settler)
    actual_mixing_time = mixer_volume / reference_flow
    actual_settling_time = settler_volume / reference_flow
    time_until_permanent_state = (actual_mixing_time + actual_settling_time) * condition.n_cells
    wasted_ree = condition.mass_of_reo_product_at_feed * aq_flow_rate * time_until_permanent_state
    return actual_settling_time, wasted_ree

@ur.wraps(('kg'), (None, None, None))
def calculate_ree_loss(wasted_ree_until_permanent_state: Number, total_aq_volume: Number, condition: Condition) -> Number:
    """
    It assumes that all ree in the loaded organic won't be recovered/recycled.
    """
    loss_on_operation = condition.mass_of_reo_product_at_feed * total_aq_volume
    return loss_on_operation + wasted_ree_until_permanent_state

@ur.wraps(('L'), (None, None, None, None, None, None))
def calculate_extractant_loss(settling_time: Number, settler, total_aq_volume: Number,
                              condition: Condition, extractant: Extractant, volume_of_stripping_section: Number) -> Number:
    """
    - No method for estimation of drag loss and crude loss are yet implemented.
    - It assumes that only the free ion of the extractant is capable of migrating to aqueous phase.
    - It assumes that acid-base equilibrium is the only equilibrium that would lead to formation of the extractant free ion.
    - It assumes that acid-base equilibrium of the extractant is instantaneous.
    """
    entrainment_loss = Q('0 kg')
    crud_loss = Q('0 kg')
    volatilization_loss = Q('0 kg')

    complexed_extractant_at_raffinate = REE_EXTRACTANT_STOICHIOMETRIC_PROPORTION * condition.ao_ratio * (condition.moles_of_ree_product_at_feed - condition.moles_of_ree_product_at_raffinate)
    free_extractant_at_raffinate = extractant.molar_concentration - complexed_extractant_at_raffinate
    ionized_extractants_at_raffinate = Ka_from_pKa(extractant.pKa) / (Ka_from_pKa(extractant.pKa) + H_from_pH(condition.pH_at_raffinate)) * free_extractant_at_raffinate
    extraction_solubilization_loss = ionized_extractants_at_raffinate * total_aq_volume * extractant.molecular_weight

    free_extractant_at_stripping_raffinate = extractant.molar_concentration - ionized_extractants_at_raffinate
    ionized_extractants_at_stripping_raffinate = Ka_from_pKa(extractant.pKa) / (Ka_from_pKa(extractant.pKa) + STRIPPING_SOLUTION_ACID_CONCENTRATION) * free_extractant_at_stripping_raffinate
    stripping_solubilization_loss = ionized_extractants_at_stripping_raffinate * volume_of_stripping_section * extractant.molecular_weight

    solubilization_loss = extraction_solubilization_loss + stripping_solubilization_loss

    # - It assumes that volatilization occurs only at the settler, not at the tanks nor the mixer nor anywhere else.
    """ volatilization_loss = (area_of_rectangle(settler['HEIGHT'], settler['WIDTH'])
                           * extractant.volatilization_rate
                           * extractant.volumetric_concentration
                           * settling_time) """

    return (entrainment_loss + crud_loss + solubilization_loss + volatilization_loss) / extractant.density

@ur.wraps(('L'), (None, None, None))
def calculate_solvent_loss(total_aq_volume: Number, solvent: Solvent, volume_of_stripping_section: Number) -> Number:
    """
    - No method for estimation of drag loss, crude loss and volatilization loss are yet implemented.
    """
    entrainment_loss = Q('0 kg')
    crud_loss = Q('0 kg')
    volatilization_loss = Q('0 kg')
    solubilization_loss = solvent.solubility_in_water * (total_aq_volume + volume_of_stripping_section)

    return (entrainment_loss + crud_loss + solubilization_loss + volatilization_loss) / solvent.density

@ur.wraps(('L', 'L'), (None, None, None))
def calculate_acid_loss(total_aq_volume: Number, ao_ratio: Number, pHi: Number) -> tuple[Number, Number]:
    """
    It assumes that the stripping solution is enough to clear organic phase from REEs.
    It assumes that the acid and the rees are herewith lost.

    Hence, the stripping volume equals the organic phase volume times the number of times it circulates
    times the A/O ratio between stripping solution and organic phase.

    The total volume of organic that passes through the stripping section equals organic flow rate times the time reference
    or the total aqueous volume divided by A/O ratio.
    """
    acid_to_pHi = (total_aq_volume * Q(H_from_pH(pHi), 'mol/L') / HCL['MOLAR_CONCENTRATION'])

    volume_of_stripping_section = total_aq_volume * (AO_RATIO_IN_STRIPPING_SECTION / ao_ratio)
    acid_to_stripping = volume_of_stripping_section * (STRIPPING_SOLUTION_ACID_CONCENTRATION / HCL['MOLAR_CONCENTRATION'])

    return acid_to_pHi + acid_to_stripping, volume_of_stripping_section
