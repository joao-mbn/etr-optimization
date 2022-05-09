from typing import Any

from helpers._common import volume_of_parallelepiped
from helpers._utils import value_or_default, weighted_average
from static_values._equipments import (AGITATORS, LEVEL_CONTROLLERS,
                                       LEVEL_INDICATORS, MIXER_SETTLERS, PIPES,
                                       PUMPS, TANKS)
from static_values._miscellaneous import (HEAD_LOSS_BETWEEN_CELLS,
                                          PHASE_SETTLING_TIME,
                                          REE_SX_EQUILIBRIUM_TIME)
from static_values._substances import WATER
from templates._types import Number

from cost._energy import (calculate_required_agitator_power,
                          calculate_required_pump_power, calculate_rpm)


def get_equipments(aq_flow_rate: Number, org_flow_rate: Number, reference_flow_rate: Number, extractant, solvent, ao_ratio: Number):

    org_avg_density = weighted_average([extractant['DENSITY'], solvent['DENSITY']], [extractant['CONCENTRATION'], 1 - extractant['CONCENTRATION']])

    cell = get_adequate_cell(reference_flow_rate)
    pipe = get_adequate_pipe()
    aq_pump, aq_pump_operating_power = get_adequate_pump(aq_flow_rate, WATER['DENSITY'], pipe['DIAMETER'])
    org_pump, org_pump_operating_power = get_adequate_pump(org_flow_rate, org_avg_density, pipe['DIAMETER'])
    agitator, agitator_operating_power = get_adequate_agitator(aq_flow_rate, org_flow_rate, org_avg_density, ao_ratio)
    level_indicator = get_adequate_level_indicator()
    level_controller = get_adequate_level_controller()
    tank = get_adequate_tank()

    return dict(
        cell=cell,
        agitator=agitator,
        aq_pump=aq_pump,
        org_pump=org_pump,
        pipe=pipe,
        level_indicator=level_indicator,
        level_controller=level_controller,
        tank=tank
    ), dict(
        aq_pump_operating_power=aq_pump_operating_power,
        org_pump_operating_power=org_pump_operating_power,
        agitator_operating_power=agitator_operating_power
    )

def get_adequate_cell(reference_flow_rate: Number):
    smallest_mixer_possible = reference_flow_rate * REE_SX_EQUILIBRIUM_TIME # Volume in L
    smallest_settler_possible = reference_flow_rate * PHASE_SETTLING_TIME   # Volume in L

    big_enough_cells: list[Any] = []
    for cell in MIXER_SETTLERS:
        mixer, settler = cell['MIXER'], cell['SETTLER']
        mixer_volume = value_or_default(mixer, 'VOLUME', volume_of_parallelepiped(mixer['HEIGHT'], mixer['WIDTH'], mixer['DEPTH']))
        settler_volume = value_or_default(settler, 'VOLUME', volume_of_parallelepiped(settler['HEIGHT'], settler['WIDTH'], settler['DEPTH']))
        if mixer_volume >= smallest_mixer_possible and settler_volume >= smallest_settler_possible:
            big_enough_cells.append(cell)

    big_enough_cells.sort(key=lambda cell: cell['PRICE'])
    cheapest_cell = big_enough_cells[0]
    return cheapest_cell

def get_adequate_pump(flow_rate: Number, fluid_density: Number, pipe_diameter: Number):
    """
    Selection method could be refined to select not only to select the cheapest in capital cost,
    but to select the cheapest in the aggregate of combined capital cost and power consumption over a period of time.
    """
    required_power = calculate_required_pump_power(flow_rate, fluid_density, pipe_diameter)
    powerful_enough_pumps = next((pump for pump in PUMPS if pump['MAX_POWER'] >= required_power / pump['EFFICIENCY']))
    powerful_enough_pumps.sort(key=lambda pump: pump['PRICE'])
    cheapest_pump = powerful_enough_pumps[0]
    operating_power = required_power / cheapest_pump
    return cheapest_pump, operating_power

def get_adequate_agitator(aq_flow_rate: Number, org_flow_rate: Number, org_avg_density: Number, ao_ratio: Number):
    """
    Selection method could be refined to select not only to select the cheapest in capital cost,
    but to select the cheapest in the aggregate of combined capital cost and power consumption over a period of time.
    """
    mixture_avg_flow_rate = weighted_average([org_flow_rate, aq_flow_rate], [1, ao_ratio])
    mixture_avg_density = weighted_average([org_avg_density, WATER['DENSITY']], [1, ao_ratio])
    required_power = calculate_required_agitator_power(mixture_avg_flow_rate, mixture_avg_density, HEAD_LOSS_BETWEEN_CELLS)

    adequate_agitators: list[Any] = []
    for agitator in AGITATORS:
        operating_power = required_power / agitator['EFFICIENCY']
        rpm = calculate_rpm(agitator['OPTIMAL_TORQUE'], operating_power)
        if agitator['MAX_POWER'] >= operating_power and agitator['MAX_RPM'] > rpm:
            adequate_agitators.append(agitator)

    adequate_agitators.sort(key=lambda agitator: agitator['PRICE'])
    cheapest_agitator = adequate_agitators[0]
    operating_power = required_power / cheapest_agitator['EFFICIENCY']
    return cheapest_agitator

def get_adequate_pipe():
    """
    There isn't yet a criteria for pipe selection.
    Knowledge of the pipe is necessary to estimate fluid velocity, which is used to estimate pump's power.
    """
    return PIPES[0]

def get_adequate_level_indicator():
    """
    There isn't yet a criteria for level indicator selection.
    """
    return LEVEL_INDICATORS[0]

def get_adequate_level_controller():
    """
    There isn't yet a criteria for level controller selection.
    """
    return LEVEL_CONTROLLERS[0]

def get_adequate_tank():
    """
    There isn't yet a criteria for tank selection.
    """
    return TANKS[0]
