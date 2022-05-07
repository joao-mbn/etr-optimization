TOTAL_PRODUCTION = 100 # ton/year Ree

PRICES = {
    'EXTRACTANTS': {
        'P507': 1,
        'D2EHPA': 1,
        'CYANEX_572': 1,
    },
    'ISOPARAFFIN': 1,
    'HCL': 1,
}

MIXER_SETTLERS = {
    1: {
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
    2: {
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
    3: {
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
}

HCL_DENSITY = 1.17 # g/mL
HCL_MOLAR_MASS = 35.453 # g/mol
HCL_VOLUMETRIC_CONCENTRATION = 0.37 # v/v
HCL_MOLAR_CONCENTRATION = 1000 * HCL_VOLUMETRIC_CONCENTRATION * HCL_DENSITY / HCL_MOLAR_MASS

REE_SX_EQUILIBRIUM_TIME = 15 # min
PHASE_SETTLING_TIME = 10 # min