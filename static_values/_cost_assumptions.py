TOTAL_PRODUCTION = 100 # ton/year Ree

ENERGY_COST_PER_KWH = 0.1 # $/kWh
OPERATORS_COST = 1
HCL_PRICE = 1 # $/ton

FEED_LIQUOR = {
    'PRICE': 1,
}

ISOPARAFFIN = {
    'PRICE': 1
}

MIXER_SETTLERS = [
    {
        'PRICE': 1,
        'MIXER': {
            'HEIGHT': 1,
            'WIDTH': 1,
            'DEPTH': 1,
        },
        'SETTLER': {
            'HEIGHT': 1,
            'WIDTH': 1,
            'DEPTH': 1,
        }
    },
    {
        'PRICE': 1,
        'MIXER': {
            'HEIGHT': 1,
            'WIDTH': 1,
            'DEPTH': 1,
        },
        'SETTLER': {
            'HEIGHT': 1,
            'WIDTH': 1,
            'DEPTH': 1,
        }
    },
    {
        'PRICE': 1,
        'MIXER': {
            'HEIGHT': 1,
            'WIDTH': 1,
            'DEPTH': 1,
        },
        'SETTLER': {
            'HEIGHT': 1,
            'WIDTH': 1,
            'DEPTH': 1,
        }
    }
]

HCL_DENSITY = 1.17 # g/mL
HCL_MOLAR_MASS = 35.453 # g/mol
HCL_VOLUMETRIC_CONCENTRATION = 0.37 # v/v
HCL_MOLAR_CONCENTRATION = 1000 * HCL_VOLUMETRIC_CONCENTRATION * HCL_DENSITY / HCL_MOLAR_MASS

REE_SX_EQUILIBRIUM_TIME = 15 # min
PHASE_SETTLING_TIME = 10 # min