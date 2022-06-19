from templates._units import quantity as Q

TIME_REFERENCE = Q(1, 'year') # Assumed
PRODUCTION_RATE = Q(10, 'ton/year') # Assumed
TOTAL_PRODUCTION = TIME_REFERENCE * PRODUCTION_RATE
INTEREST_RATE_ON_CAPITAL = Q(0.1, 'year^-1') # Assumed

# Considering approximations and values not considered.
# e.g. FOB to CIF, price of water, stage efficiency, extra energy from headlosses, equipment for stripping and so on.
MARGIN_OF_SAFETY = Q(1.5) # Assumed

# COSTS ==================================================================

# From Minas Gerais' price with 1 USD = 5 BRL as conversion ratio.
# https://www.poder360.com.br/energia/rio-de-janeiro-lidera-ranking-de-custo-de-energia-a-industria/#:~:text=Dados%20de%20um%20levantamento%20da,%24%20736%2C78%2FMWh.
ENERGY_COST = Q('143.2 usd/MWh')
# Estimated from salaries of CBMM operators on Glassdoor: https://www.glassdoor.com.br/Sal%C3%A1rio/Companhia-Brasileira-de-Metalurgia-e-Minera%C3%A7%C3%A3o-CBMM-Sal%C3%A1rios-E808543.htm
# plus estimation of expenses with feeding, transportation and health care.
OPERATOR_COST = Q('20000 usd/year')
# ========================================================================

# Equilibrium
# Estimated based on Qi's reports
# QI, D.,  Hydrometallurgy of Rare Earths, [S.l.], Elsevier, 2018. p. 187–389. DOI: 10.1016/B978-0-12-813920-2.00002-7.
REE_SX_EQUILIBRIUM_TIME = Q('10 min')
PHASE_SETTLING_TIME = Q('10 min') # Overestimation of what has been seen on bench scale experiments
# ========================================================================


# Constants
ACCELERATION_OF_GRAVITY = Q('9.81 m/s^2') # https://en.wikipedia.org/wiki/Gravity_of_Earth
# ========================================================================

# Distances of Equipment
DISTANCE_BETWEEN_ORG_TANK_AND_RAFFINATE_CELL = Q('1 m') # Assumed
DISTANCE_BETWEEN_AQ_TANK_AND_FEED_CELL = Q('1 m') # Assumed
DISTANCE_BETWEEN_STRIPPING_SOLUTION_TANK_AND_STRIPPING_FEED_CELL = Q('1 m') # Assumed
DISTANCE_BETWEEN_CELLS = Q('0 m') # Assuming that coupled cells are being used. See: https://www.meab-mx.se/pdf/msu_0_5.pdf
# ========================================================================

# Assumed values for efficiencies, since it hasn't been specified by any seller.
AGITATOR_EFFICIENCY = Q(0.7) # Assumed
PUMP_EFFICIENCY = Q(0.7) # Assumed
# ========================================================================

# Others
NUMBER_OF_CELLS_IN_STRIPPING_SECTION = Q(3) # Overestimation of what has been seen on bench scale experiments.
AO_RATIO_IN_STRIPPING_SECTION = Q(1) # Commonly used ratio when no previous optimization has been conducted.
# Estimated based on Qi's reports
# # QI, D.,  Hydrometallurgy of Rare Earths, [S.l.], Elsevier, 2018. p. 187–389. DOI: 10.1016/B978-0-12-813920-2.00002-7.
STRIPPING_SOLUTION_ACID_CONCENTRATION = Q('3 mol/L')

HEAD_LOSS_BETWEEN_CELLS = Q('0.1 m') # Assumed

# Conservative estimation of the number of operators necessary to cover 1 position at a 24/7 production.
# https://www.callcentrehelper.com/question-what-is-the-minimum-number-of-staff-required-for-a-24-hour-call-centre-2039.htm
# https://www.quora.com/How-many-employees-do-I-need-to-cover-24-7
NUMBER_OF_OPERATORS_PER_POSITION = Q(6)
NUMBER_OF_POSITIONS = Q(1)