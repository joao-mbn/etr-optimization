from templates._units import quantity as Q

TIME_REFERENCE = Q('1 year')
TOTAL_PRODUCTION = Q('1 ton')

STRIPPING_SOLUTION_ACID_CONCENTRATION = Q('3 mol/L')
HEAD_LOSS_BETWEEN_CELLS = Q('0.1 m')

# Costs
ENERGY_COST_PER_KWH = Q('0.1 usd/kWh')
OPERATORS_COST = Q('0.1 usd')

# Equilibrium
REE_SX_EQUILIBRIUM_TIME = Q('15 min')
PHASE_SETTLING_TIME = Q('10 min')

# Constants
ACCELERATION_OF_GRAVITY = Q('9.81 m/s^2')

# Distances of Equipment
DISTANCE_BETWEEN_ORG_TANK_AND_RAFFINATE_CELL = Q('1 m')
DISTANCE_BETWEEN_AQ_TANK_AND_FEED_CELL = Q('1 m')
DISTANCE_BETWEEN_CELLS = Q('1 m')