from templates._units import quantity as Q

TIME_REFERENCE = Q(10, 'year')
YEARLY_PRODUCTION = Q(10, 'ton/year')
TOTAL_PRODUCTION = TIME_REFERENCE * YEARLY_PRODUCTION

# Considering approximations and values not considered.
# e.g. FOB to CIF, price of water, stage efficiency, extra energy from headlosses, equipment for stripping and so on.
MARGIN_OF_SAFETY = Q(1.5)

# Costs
ENERGY_COST = Q('145 usd/MWh')
OPERATOR_COST = Q('20000 usd/year') # Estimated from salaries of CBMM operators on Glassdoor, plus estimation of expenses with feeding, transportation and health care.

# Equilibrium
REE_SX_EQUILIBRIUM_TIME = Q('15 min')
PHASE_SETTLING_TIME = Q('10 min')

# Constants
ACCELERATION_OF_GRAVITY = Q('9.81 m/s^2')

# Distances of Equipment
DISTANCE_BETWEEN_ORG_TANK_AND_RAFFINATE_CELL = Q('1 m')
DISTANCE_BETWEEN_AQ_TANK_AND_FEED_CELL = Q('1 m')
DISTANCE_BETWEEN_STRIPPING_SOLUTION_TANK_AND_STRIPPING_FEED_CELL = Q('1 m')
DISTANCE_BETWEEN_CELLS = Q('0 m') # Assuming that coupled cells are being used. See: https://www.meab-mx.se/pdf/msu_0_5.pdf

# Assumed values for efficiencies
STAGE_EFFICIENCY = Q(1)
AGITATOR_EFFICIENCY = Q(0.7)
PUMP_EFFICIENCY = Q(0.7)

# Others
NUMBER_OF_CELLS_IN_STRIPPING_SECTION = 3
STRIPPING_SOLUTION_ACID_CONCENTRATION = Q('3 mol/L')
HEAD_LOSS_BETWEEN_CELLS = Q('0.1 m') # Guessed
NUMBER_OF_OPERATORS = Q(6) # Conservative estimation of the number of operators necessary to cover 1 position at a 24/7 production.