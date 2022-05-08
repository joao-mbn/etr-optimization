from typing import Any

from helpers._common import volume
from helpers._utils import value_or_default
from static_values._cost_assumptions import (MIXER_SETTLERS,
                                             PHASE_SETTLING_TIME,
                                             REE_SX_EQUILIBRIUM_TIME)
from templates._types import Number

def get_equipments(aq_flow_rate: Number, org_flow_rate: Number, reference_flow_rate: Number):

    cell = get_adequate_cell(reference_flow_rate)

    # TODO ZONE
    agitator = get_adequate_agitator()
    aq_pump = get_adequate_pump(aq_flow_rate)
    org_pump = get_adequate_pump(org_flow_rate)
    pipe = get_adequate_pipe()
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
    )

def get_adequate_cell(reference_flow_rate: Number):
    smallest_mixer_possible = reference_flow_rate * REE_SX_EQUILIBRIUM_TIME # Volume in L
    smallest_settler_possible = reference_flow_rate * PHASE_SETTLING_TIME   # Volume in L
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

def get_adequate_pipe():
    pass

def get_adequate_level_indicator():
    pass

def get_adequate_level_controller():
    pass

def get_adequate_tank():
    pass
