from helpers._common import H_from_pH, g_in_ton, minutes_in_year, volume
from static_values._cost_assumptions import (HCL_MOLAR_CONCENTRATION,
                                             PHASE_SETTLING_TIME,
                                             REE_SX_EQUILIBRIUM_TIME,
                                             TOTAL_PRODUCTION)
from templates._types import Number


def calculate_cost(condition, extractant) -> Number:

    preliminary_calculations(condition, extractant)

    return capital_cost() + operating_cost()

def preliminary_calculations(condition, extractant):

    # Note: Note all keys actually exist in the condition dictionary

    # Annual Volumes Output (L/year)

        # Wasted
    total_aq_volume = g_in_ton(TOTAL_PRODUCTION) / condition['product_concentration_in_raffinate']
    acid_volume = total_aq_volume * H_from_pH(condition['pHi']) / HCL_MOLAR_CONCENTRATION

        # Inventory
    total_org_volume = total_aq_volume / condition['ao_ratio']
    extractant_volume = total_org_volume / extractant['concentration'] / extractant['purity']
    solvent_volume = total_org_volume - extractant_volume

    # Flow rates (L/min)
    aq_flow_rate = total_aq_volume / minutes_in_year(1)
    org_flow_rate = total_org_volume / minutes_in_year(1)

    # Equipment Dimensions

        # The fastest flow should still have a residence time great enough to meet equilibrium
    reference_flow = max(aq_flow_rate, org_flow_rate)

    smallest_mixer_possible = reference_flow * REE_SX_EQUILIBRIUM_TIME
    smallest_settler_possible = reference_flow * PHASE_SETTLING_TIME
    cell = get_adequate_mixer_settler(smallest_mixer_possible, smallest_settler_possible)

    # Equilibrium Times (min)

    mixer = cell['MIXER']
    settler = cell['SETTLER']

    actual_mixing_time = volume(mixer['HEIGHT'], mixer['WIDTH'], mixer['DEPTH']) / reference_flow
    actual_settling_time = volume(settler['HEIGHT'], settler['WIDTH'], settler['DEPTH']) / reference_flow
    time_until_permanent_state = (actual_mixing_time + actual_settling_time) * condition['n_cells']
    wasted_ree = condition['aq_feed_concentration'] * time_until_permanent_state

    # Pump Calculations
        # based on price, efficiency and potency requirements

    needed_energy = 0 # energy for the pumps and mixers

    aq_pump = get_adequate_pump(aq_flow_rate)
    org_pump = get_adequate_pump(org_flow_rate)

    pass


















def get_adequate_mixer_settler(smallest_mixer_possible: Number, smallest_settler_possible: Number) -> Number:
    pass

def get_adequate_pump(flow_rate: Number) -> Number:
    pass

def capital_cost() -> Number:
    pass

def operating_cost(total_aq_volume = 1) -> Number:

    return (
        ree_loss_per_liter()
        + extractant_loss_per_liter()
        + solvent_loss_per_liter()
    ) * total_aq_volume + energy_cost()

def ree_loss_per_liter() -> Number:
    loss_loaded_organic = 0
    pass

def extractant_loss_per_liter() -> Number:
    drag_loss = 0
    crude_loss = 0
    dissociation_loss = 0
    volatilization_loss = 0
    pass

def solvent_loss_per_liter() -> Number:
    drag_loss = 0
    crude_loss = 0
    dissociation_loss = 0
    volatilization_loss = 0
    pass

def energy_cost() -> Number:
    pump_energy_consumption = 0
    mixer_energy_consumption = 0
    pass
