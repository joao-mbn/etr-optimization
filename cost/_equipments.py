from typing import Any

import numpy as np
from helpers._common import volume_of_mixer_settler
from helpers._utils import value_or_default, weighted_average
from static_values._equipments import (FLOW_CONTROLLERS, FLOW_SENSORS,
                                       MIXER_SETTLERS,
                                       PH_SENSOR_AND_TRANSMITTER, PIPES, PUMPS,
                                       TANKS)
from static_values._miscellaneous import (
    AGITATOR_EFFICIENCY, DISTANCE_BETWEEN_AQ_TANK_AND_FEED_CELL,
    DISTANCE_BETWEEN_CELLS, DISTANCE_BETWEEN_ORG_TANK_AND_RAFFINATE_CELL,
    DISTANCE_BETWEEN_STRIPPING_SOLUTION_TANK_AND_STRIPPING_FEED_CELL,
    HEAD_LOSS_BETWEEN_CELLS, NUMBER_OF_CELLS_IN_STRIPPING_SECTION,
    PHASE_SETTLING_TIME, PUMP_EFFICIENCY, REE_SX_EQUILIBRIUM_TIME)
from static_values._substances import WATER
from templates._classes import Extractant, Solvent
from templates._models import Condition
from templates._types import Number
from templates._units import quantity as Q

from cost._energy import (calculate_required_agitator_power,
                          calculate_required_pump_power)


def get_equipments(aq_flow_rate: Number, org_flow_rate: Number, reference_flow_rate: Number, total_flow_rate: Number,
                   extractant: Extractant, solvent: Solvent, condition: Condition) -> tuple[Any, dict[str, Number], Number]:

    """
    - It assumes that the total volume of the phase is equal to the sum of the volume of its individual components, an ideal fluid.
    - It assumes that the two phases do not need to be controlled, only the A/O ratio.
    """
    org_avg_density = weighted_average([extractant.density, solvent.density],
                                       [extractant.volumetric_concentration, solvent.volumetric_concentration])

    cell, cell_operating_power = get_adequate_mixer_settler(total_flow_rate, reference_flow_rate, aq_flow_rate, org_flow_rate, org_avg_density, condition.ao_ratio)
    pipe, total_pipe_length, pipe_diameter = get_adequate_pipe(condition.n_cells)
    aq_pump, aq_pump_operating_power = get_adequate_pump(aq_flow_rate, WATER['DENSITY'], pipe_diameter)
    org_pump, org_pump_operating_power = get_adequate_pump(org_flow_rate, org_avg_density, pipe_diameter)

    # It assumes that the stripping occurs with A/O ratio 1, between stripping solution and organic phase.
    stripping_solution_pump, stripping_solution_pump_operating_power = get_adequate_pump(org_flow_rate, WATER['DENSITY'], pipe_diameter)

    pH_sensor_transmitter = get_adequate_pH_sensor_transmitter()
    aq_flow_indicator, org_flow_indicator = get_adequate_flow_indicator(), get_adequate_flow_indicator()
    aq_flow_controller, concentrated_acid_flow_controller = get_adequate_flow_controller(), get_adequate_flow_controller()
    aq_tank, org_tank, stripping_tank = get_adequate_tank(), get_adequate_tank(), get_adequate_tank()

    equipments = dict(
        cell=cell,
        aq_pump=aq_pump,
        org_pump=org_pump,
        stripping_solution_pump=stripping_solution_pump,
        pipe=pipe,
        pH_sensor_transmitter=pH_sensor_transmitter,
        aq_flow_indicator=aq_flow_indicator,
        org_flow_indicator=org_flow_indicator,
        aq_flow_controller=aq_flow_controller,
        concentrated_acid_flow_controller=concentrated_acid_flow_controller,
        aq_tank=aq_tank,
        org_tank=org_tank,
        stripping_tank=stripping_tank,
    )

    operating_powers = dict(
        aq_pump_operating_power=aq_pump_operating_power,
        org_pump_operating_power=org_pump_operating_power,
        cell_operating_power=cell_operating_power,
        stripping_solution_pump_operating_power=stripping_solution_pump_operating_power,
    )

    return equipments, operating_powers, total_pipe_length

def get_adequate_mixer_settler(total_flow_rate: Number, reference_flow_rate: Number, aq_flow_rate: Number, org_flow_rate: Number,
                               org_avg_density: Number, ao_ratio: Number):

    smallest_mixer_possible, smallest_settler_possible = mixer_settler_required_size(reference_flow_rate)
    required_power = mixer_settler_required_power(aq_flow_rate, org_flow_rate, org_avg_density, ao_ratio)
    operating_power = required_power / AGITATOR_EFFICIENCY

    adequate_cells: list[Any] = []
    for cell in MIXER_SETTLERS:

        mixer, settler = cell['MIXER'], cell['SETTLER']
        mixer_volume, settler_volume = volume_of_mixer_settler(mixer, settler)

        recommended_flow = value_or_default(cell, 'RECOMMENDED_FLOW', Q(-np.inf, 'L/min'))
        agitator_powerful_enough = (value_or_default(cell, 'MAX_POWER', Q(-np.inf, 'W')) >= operating_power or
                                    value_or_default(cell, 'MAX_FLOW', Q(-np.inf, 'L/min')) >= total_flow_rate or
                                    (recommended_flow * 1.5 >= total_flow_rate and recommended_flow * 0.5 <= total_flow_rate))

        if (mixer_volume >= smallest_mixer_possible and settler_volume >= smallest_settler_possible and agitator_powerful_enough):
            adequate_cells.append(cell)

    adequate_cells.sort(key=lambda cell: cell['PRICE'])
    cheapest_cell = adequate_cells[0]
    return cheapest_cell, operating_power

def mixer_settler_required_size(reference_flow_rate: Number) -> Number:
    smallest_mixer_possible = reference_flow_rate * REE_SX_EQUILIBRIUM_TIME
    smallest_settler_possible = reference_flow_rate * PHASE_SETTLING_TIME
    return smallest_mixer_possible, smallest_settler_possible

def mixer_settler_required_power(aq_flow_rate: Number, org_flow_rate: Number, org_avg_density: Number, ao_ratio: Number):
    """
    Selection method could be refined to select not only to select the cheapest in capital cost,
    but to select the cheapest in the aggregate of combined capital cost and power consumption over a period of time.
    """
    mixture_avg_flow_rate = weighted_average([org_flow_rate, aq_flow_rate], [1, ao_ratio])
    mixture_avg_density = weighted_average([org_avg_density, WATER['DENSITY']], [1, ao_ratio])
    required_power = calculate_required_agitator_power(mixture_avg_flow_rate, mixture_avg_density, HEAD_LOSS_BETWEEN_CELLS)
    return required_power

def get_adequate_pump(flow_rate: Number, fluid_density: Number, pipe_diameter: Number):
    """
    Selection method could be refined to select not only to select the cheapest in capital cost,
    but to select the cheapest in the aggregate of combined capital cost and power consumption over a period of time.
    """
    powerful_enough_pumps: list[dict[str, Any]] = []
    required_power = calculate_required_pump_power(flow_rate, fluid_density, pipe_diameter)
    operating_power = required_power / PUMP_EFFICIENCY

    for pump in PUMPS:

        operating_power_range = value_or_default(pump, 'OPERATING_POWER_RANGE', (Q(0, 'W'), Q(0, 'W')))

        if (value_or_default(pump, 'MAX_POWER', Q(-np.inf, 'W')) >= operating_power or
            value_or_default(pump, 'MAX_FLOW', Q(-np.inf, 'L/min')) >= flow_rate or
            (required_power >= operating_power_range[0] and required_power <= operating_power_range[1])):

            powerful_enough_pumps.append(pump)

    powerful_enough_pumps.sort(key=lambda pump: pump['PRICE'])
    cheapest_pump = powerful_enough_pumps[0]
    return cheapest_pump, operating_power

def get_adequate_pipe(n_cells: int):
    """
    Knowledge of the pipe is necessary to estimate fluid velocity, which is used to estimate pump's power.
    The smallest power required will be in the condition with the greatest pipe diameter.
    As a first approximation, the greatest diameter available was chosen regardless of any other factors.
    """
    pipe_length_aq = n_cells * DISTANCE_BETWEEN_CELLS + DISTANCE_BETWEEN_AQ_TANK_AND_FEED_CELL
    pipe_length_org = n_cells * DISTANCE_BETWEEN_CELLS + DISTANCE_BETWEEN_ORG_TANK_AND_RAFFINATE_CELL
    pipe_length_stripping = NUMBER_OF_CELLS_IN_STRIPPING_SECTION * DISTANCE_BETWEEN_CELLS + DISTANCE_BETWEEN_STRIPPING_SOLUTION_TANK_AND_STRIPPING_FEED_CELL
    total_pipe_length = pipe_length_aq + pipe_length_org + pipe_length_stripping
    PIPES.sort(key=lambda pipe: pipe['DIAMETER_RANGE'][1], reverse=True)
    best_pipe = PIPES[0]
    return best_pipe, total_pipe_length, best_pipe['DIAMETER_RANGE'][1]

def get_adequate_pH_sensor_transmitter():
    """
    There isn't yet a criteria for pH indicator selection.
    """
    PH_SENSOR_AND_TRANSMITTER.sort(key=lambda sensor: sensor['PRICE'])
    return PH_SENSOR_AND_TRANSMITTER[0]

def get_adequate_flow_indicator():
    """
    There isn't yet a criteria for level indicator selection.
    """
    FLOW_SENSORS.sort(key=lambda sensor: sensor['PRICE'])
    return FLOW_SENSORS[0]

def get_adequate_flow_controller():
    """
    There isn't yet a criteria for level controller selection.
    """
    FLOW_CONTROLLERS.sort(key=lambda controller: controller['PRICE'])
    return FLOW_CONTROLLERS[0]

def get_adequate_tank():
    """
    There isn't yet a criteria for tank selection.
    """
    TANKS.sort(key=lambda tank: tank['PRICE'])
    return TANKS[0]
