from templates._units import quantity as Q

PIPES = [
    {
        'DIAMETER': Q('0.5 mm'),
        'PRICE_PER_LENGTH': Q('0.1 usd/m'),
    }
]

PUMPS = [
    {
        'PRICE': Q('0.1 usd'),
        'EFFICIENCY': Q('0.9'),
        'MAX_POWER': Q('100 kW'),
    },
    {
        'PRICE': Q('0.2 usd'),
        'EFFICIENCY': Q('0.6'),
        'MAX_POWER': Q('300 kW'),
    }
]

MIXER_SETTLERS = [
    {
        'PRICE': Q('10000 usd'),
        'MIXER': {
            'HEIGHT': Q('2 m'),
            'WIDTH': Q('10 m'),
            'DEPTH': Q('2 m'),
        },
        'SETTLER': {
            'HEIGHT': Q('1 m'),
            'WIDTH': Q('1 m'),
            'DEPTH': Q('1 m'),
        }
    },
    {
        'PRICE': Q('8000 usd'),
        'MIXER': {
            'HEIGHT': Q('1 m'),
            'WIDTH': Q('1 m'),
            'DEPTH': Q('1 m'),
        },
        'SETTLER': {
            'HEIGHT': Q('1 m'),
            'WIDTH': Q('1 m'),
            'DEPTH': Q('1 m'),
        }
    },
    {
        'PRICE': Q('7000 usd'),
        'MIXER': {
            'HEIGHT': Q('1 m'),
            'WIDTH': Q('1 m'),
            'DEPTH': Q('1 m'),
        },
        'SETTLER': {
            'HEIGHT': Q('1 m'),
            'WIDTH': Q('1 m'),
            'DEPTH': Q('1 m'),
        }
    }
]

AGITATORS = [
    {
        'PRICE': Q('0.1 usd'),
        'EFFICIENCY': Q('0.9'),
        'MAX_POWER': Q('100 kW'),
        'MAX_RPM': Q('100 rpm'),
        'OPTIMAL_TORQUE': Q('100 N m'),
    }
]

LEVEL_INDICATORS = [
    {
        'PRICE': Q('0.1 usd'),
    }
]

LEVEL_CONTROLLERS = [
    {
        'PRICE': Q('0.1 usd'),
    }
]

TANKS = [
    {
        'PRICE': Q('0.1 usd'),
    }
]