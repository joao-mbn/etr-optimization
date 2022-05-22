import math as m

from helpers._common import area_of_circle
from static_values._miscellaneous import ACCELERATION_OF_GRAVITY, TIME_REFERENCE
from templates._types import Number
from templates._units import unit_registry as ur

@ur.wraps(('kWh'), (None, None, None, None))
def energy_consumption(n_cells: int, aq_pump_operating_power: Number,
                       org_pump_operating_power: Number, agitator_operating_power: Number) -> Number:

    return TIME_REFERENCE * (aq_pump_operating_power + org_pump_operating_power + agitator_operating_power * n_cells)

@ur.wraps(('kilowatt'), (None, None, None))
def calculate_required_pump_power(flow_rate, fluid_density, pipe_diameter) -> Number:
    """
    This calculates the power required to pump the fluid from the tanks to the cell.

    It assumes:
        - no change in pressure (both 1 atm)
        - initial velocity is 0
        - no change in height (the tanks are at the same height as any cell)
        - there is no head loss
            - fluid is ideal, hence zero viscosity and no resistance to shear stress

    References:

    See Bernoulli's Principle.

    https://en.wikipedia.org/wiki/Bernoulli%27s_principle \n
    https://www.electrical4u.net/energy-calculation/pump-power-calculator-formula-example-calculation/ \n
    https://www.youtube.com/watch?v=ZTCc88D2HAc
    """
    pipe_cross_section = area_of_circle(pipe_diameter)
    final_velocity = flow_rate / pipe_cross_section
    velocity_head = final_velocity ** 2 / 2 / ACCELERATION_OF_GRAVITY
    power = velocity_head * flow_rate * fluid_density * ACCELERATION_OF_GRAVITY
    return power

@ur.wraps(('kilowatt'), (None, None, None))
def calculate_required_agitator_power(flow_rate: Number, fluid_density: Number, head_loss: Number) -> Number:
    """
    This calculates the power required to pump the fluid from one cell to another.

    It assumes:
        - no change in pressure (both 1 atm)
        - velocity within the SX circuit is kept constant
        - no change in height, the cells are kept at the same height

    References:

    See Bernoulli's Principle.

    https://en.wikipedia.org/wiki/Bernoulli%27s_principle \n
    https://www.electrical4u.net/energy-calculation/pump-power-calculator-formula-example-calculation/ \n
    https://www.youtube.com/watch?v=ZTCc88D2HAc
    """
    head_to_add = head_loss
    power = head_to_add * flow_rate * fluid_density * ACCELERATION_OF_GRAVITY
    return power

@ur.wraps(('rpm'), ('N m', 'kilowatt'))
def calculate_rpm(motor_torque: Number, operating_power: Number) -> Number:
    """
    @Deprecated - removed from calculations.

    This calculates the RPM of the agitator.
    While the pump allows you to set flow rate, which is given by the required output,
    rotation is necessary to specify the agitator and not given anywhere.

    Using a torque x efficiency chart, operate on a RPM where torque would provide highest efficiency,
    which diminishes operating power.

    See reference for such a chart.

    Reference:

    https://simplemotor.com/calculations/
    """
    return operating_power * 2 * m.pi / motor_torque
