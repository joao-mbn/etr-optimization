PIPES = [
    {
        'DIAMETER': 0.5,
        'PRICE_PER_LENGTH': 1,
    }
]

PUMPS = [
    {
        'PRICE': 1,
        'EFFICIENCY': 1,
        'MAX_POWER': 9999999999,
    },
        {
        'PRICE': 2,
        'EFFICIENCY': 0.8,
        'MAX_POWER': 1e30,
    }
]

MIXER_SETTLERS = [
    {
        'PRICE': 54200, # R$/Un.
        'MIXER': {
            'HEIGHT': 999999999999999,
            'WIDTH': 1,
            'DEPTH': 1,
        },
        'SETTLER': {
            'HEIGHT': 99999999999999999,
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

AGITATORS = [
    {
        'PRICE': 1,
        'EFFICIENCY': 1,
        'MAX_POWER': 99999999999999999,
        'MAX_RPM': 999999999999999999,
        'OPTIMAL_TORQUE': 1,
    }
]

LEVEL_INDICATORS = [
    {
        'PRICE': 1,
    }
]

LEVEL_CONTROLLERS = [
    {
        'PRICE': 1,
    }
]

TANKS = [
    {
        'PRICE': 1,
    }
]