from templates._units import quantity as Q

MIXER_SETTLERS = [
    # It was assumed that flow and power specifications were those at 1 atm, 25ºC
    # and extended to organic phase as well, since liquid is assumed ideal.
    # Mixer and settler dimensions were estimated from the ratios of the two in the pictures and the total cell dimensions.

    # For CWX series
    # https://www.alibaba.com/product-detail/Laboratory-mixer-settlers-and-extraction-equipment_60767193201.html

    # For MSU series
    # https://www.meab-mx.se/pdf/msu_sq_ind.pdf
    # https://www.meab-mx.se/pdf/msu_0_5.pdf
    {
        'NAME': 'CWX-0.3J',
        'PRICE': Q('20000 usd'),
        'MAX_FLOW': Q(18, 'L/h'),
        'MAX_POWER': Q('0.02 kW'),
        'MIXER': {
            'HEIGHT': Q('400 mm'),
            'WIDTH': Q('400 mm'),
            'DEPTH': Q('160 mm'),
        },
        'SETTLER': {
            'HEIGHT': Q('400 mm'),
            'WIDTH': Q('400 mm'),
            'DEPTH': Q('640 mm'),
        }
    },
    {
        'NAME': 'CWX-1J',
        'PRICE': Q('20000 usd'),
        'MAX_POWER': Q('0.02 kW'),
        'MAX_FLOW': Q(120, 'L/h'),
        'MIXER': {
            'HEIGHT': Q('620 mm'),
            'WIDTH': Q('630 mm'),
            'DEPTH': Q('230 mm'),
        },
        'SETTLER': {
            'HEIGHT': Q('620 mm'),
            'WIDTH': Q('630 mm'),
            'DEPTH': Q('920 mm'),
        }
    },
    {
        'NAME': 'CWX-2J',
        'PRICE': Q('20000 usd'),
        'MAX_POWER': Q('0.04 kW'),
        'MAX_FLOW': Q(460, 'L/h'),
        'MIXER': {
            'HEIGHT': Q('750 mm'),
            'WIDTH': Q('750 mm'),
            'DEPTH': Q('280 mm'),
        },
        'SETTLER': {
            'HEIGHT': Q('750 mm'),
            'WIDTH': Q('750 mm'),
            'DEPTH': Q('1120 mm'),
        },
    },
    {
        'NAME': 'CWX-8J',
        'PRICE': Q('20000 usd'),
        'MAX_POWER': Q('0.09 kW'),
        'MAX_FLOW': Q(680, 'L/h'),
        'MIXER': {
            'HEIGHT': Q('950 mm'),
            'WIDTH': Q('950 mm'),
            'DEPTH': Q('340 mm'),
        },
        'SETTLER': {
            'HEIGHT': Q('950 mm'),
            'WIDTH': Q('950 mm'),
            'DEPTH': Q('1360 mm'),
        }
    },
    {
        'NAME': 'CWX-9J',
        'PRICE': Q('20000 usd'),
        'MAX_POWER': Q('0.09 kW'),
        'MAX_FLOW': Q(880, 'L/h'),
        'MIXER': {
            'HEIGHT': Q('1000 mm'),
            'WIDTH': Q('1000 mm'),
            'DEPTH': Q('400 mm'),
        },
        'SETTLER': {
            'HEIGHT': Q('1000 mm'),
            'WIDTH': Q('1000 mm'),
            'DEPTH': Q('1600 mm'),
        }
    },
    {
        'NAME': 'MSU-15',
        'PRICE': Q('40000 usd'), # Guessed
        'RECOMMENDED_FLOW': Q(200, 'L/h'),
        'MIXER': {
            'VOLUME': Q(6, 'L')
        },
        'SETTLER': {
            'VOLUME': Q(15, 'L'),
        }
    },
    {
        'NAME': 'MSU-100',
        'PRICE': Q('40000 usd'), # Guessed
        'RECOMMENDED_FLOW': Q(825, 'L/h'),
        'MIXER': {
            'VOLUME': Q(27, 'L')
        },
        'SETTLER': {
            'VOLUME': Q(100, 'L'),
        }
    },
    {
        'NAME': 'MSU-500',
        'PRICE': Q('40000 usd'), # Guessed
        'RECOMMENDED_FLOW': Q(2500, 'L/h'),
        'MIXER': {
            'VOLUME': Q(125, 'L')
        },
        'SETTLER': {
            'VOLUME': Q(500, 'L'),
        }
    },
    {
        'NAME': 'MSU-2K',
        'PRICE': Q('40000 usd'), # Guessed
        'RECOMMENDED_FLOW': Q(6400, 'L/h'),
        'MIXER': {
            'VOLUME': Q(500, 'L')
        },
        'SETTLER': {
            'VOLUME': Q(2000, 'L'),
        }
    },
    {
        'NAME': 'MSU-4,5K',
        'PRICE': Q('40000 usd'), # Guessed
        'RECOMMENDED_FLOW': Q(12000, 'L/h'),
        'MIXER': {
            'VOLUME': Q(1000, 'L')
        },
        'SETTLER': {
            'VOLUME': Q(4500, 'L'),
        }
    },
]

PUMPS = [
    {
        'NAME': 'Seabord\'s SBS100-310',
        'PRICE': Q(1500, 'usd'),
        'MAX_FLOW': Q(3100, 'L/s'),
        'MAX_HEAD': Q(200, 'm'), # How high it can lift the liquid up. At max head, flow = 0.
        'PUMP_DISCHARGE_DIAMETER_RANGE': (Q(80, 'mm'), Q(800, 'mm')),
        'MAX_POWER': Q(60, 'hp'),
    },
    {
        'NAME': 'Shuanglian\'s 100FIU60-30',
        'PRICE': Q(620, 'usd'),
        'MAX_FLOW': Q(60, 'm^3/h'),
        'OPERATING_POWER_RANGE': (Q(11, 'kW'), Q(15, 'kW'))
    },
    {
        'NAME': 'CNP\'s ZS50',
        'PRICE': Q(682, 'usd'),
        'MAX_FLOW': Q(20, 'm^3/h'),
        'MAX_HEAD': Q(57.5, 'm'), # How high it can lift the liquid up. At max head, flow = 0.
        'OPERATING_POWER_RANGE': (Q(1.1, 'kW'), Q(5.5, 'kW'))
    },
    {
        'NAME': 'CNP\'s TD',
        'PRICE': Q(4050, 'usd'),
        'MAX_FLOW': Q(480, 'm^3/h'),
        'MAX_HEAD': Q(53.2, 'm'), # How high it can lift the liquid up. At max head, flow = 0.
        'PUMP_DISCHARGE_DIAMETER': Q(200, 'mm'),
        'OPERATING_POWER_RANGE': (Q(20, 'kW'), Q(90, 'kW'))
    },
    {
        'NAME': 'TEFLOW PUMP\'s TMC-P',
        'PRICE': Q(500, 'usd'),
        'MAX_FLOW': Q(100, 'm^3/h'),
        'MAX_HEAD': Q(80, 'm'), # How high it can lift the liquid up. At max head, flow = 0.
        'PUMP_DISCHARGE_DIAMETER_RANGE': (Q(25, 'mm'), Q(80, 'mm')),
        'OPERATING_POWER_RANGE': (Q(22, 'kW'), Q(55, 'kW'))
    },
]

PH_SENSOR_AND_TRANSMITTER = [
    {
        'PRICE': Q('700 usd'),
    },
    {
        'PRICE': Q('165 usd'),
    }
]

FLOW_SENSORS = [
    # Magnetic flow meters are desired because they head losses are comparable to a straight pipe.
    # https://www.omega.com/en-us/resources/magmeter
    {
        'MATERIALS': ['Stainless Steel'],
        'TYPE': 'MAGNETIC',
        'NAME': 'KF700FA',
        'PRICE': Q('600 usd'),
        'PRESSURE_LOSS': lambda flow: Q(0.08 if flow < Q(0.6, 'm^3/h')
                                            else 0.05 if flow < Q(1.2, 'm^3/h')
                                            else 0.035 if flow < Q(7, 'm^3/h')
                                            else 0.025,
                                        'MPa'),
        'FLOW_RANGE': (Q(0.01, 'm^3/h'), Q(800, 'm^3/h')),
        'PIPE_DIAMETER_RANGE': (Q(2, 'mm'), Q(200, 'mm')),
    },
    {
        'MATERIALS': ['Stainless Steel', 'Carbon Steel', 'PP/PVC'],
        'TYPE': 'MAGNETIC',
        'NAME': 'RS485',
        'PRICE': Q('300 usd'),
        'FLOW_RANGE': (Q(0.02, 'm^3/h'), Q(2650, 'm^3/h')),
        'PIPE_DIAMETER_RANGE': (Q(10, 'mm'), Q(250, 'mm')),
    }
]

FLOW_CONTROLLERS = [
    {
        'NAME': '150 Class PVC SS304',
        'PRICE': Q(70, 'usd'),
        'DIAMETER_RANGE': (Q(0.25, 'in'), Q(0.75, 'in'))
    },
    {
        'NAME': 'CWX-15N',
        'PRICE': Q(20, 'usd'),
        'DIAMETER_RANGE': (Q(0.25, 'in'), Q(1, 'in'))
    }
]

TANKS = [
    # PVC and PP are adequate to deal with very acidic solutions.
    {
        'NAME': 'AILUSI', # Company name
        'MATERIAL': 'PP',
        'PRICE': Q(3000, 'usd'),
        'MAX_LOADING_VOLUME': Q(5000, 'L'),
        'MAX_MIXING_SPEED': Q(72, 'rpm'),
        'MAX_POWER': Q(27, 'kW'),
    },
    {
        'NAME': 'LIENM', # Company name
        'MATERIAL': 'PP/PVC',
        'PRICE': Q(8000, 'usd'),
        'MAX_LOADING_VOLUME': Q(5000, 'L'),
        'MAX_POWER': Q(1.5, 'kW'),
    },
    {
        'NAME': 'YUALIAN\'s YPC',
        'MATERIAL': 'PP/PVC',
        'PRICE': Q(2968, 'usd'),
        'MAX_LOADING_VOLUME': Q(5000, 'L'),
        'MAX_MIXING_SPEED': Q(63, 'rpm'),
        'MAX_POWER': Q(1.5, 'kW'),
    },
]

PIPES = [
    # PVC and PVDF are adequate to deal with very acidic solutions.
    {
        'MATERIAL': 'PVDF',
        'DIAMETER_RANGE': (Q(16, 'mm'), Q(30, 'mm')),
        'PRICE_PER_LENGTH': Q(4, 'usd/m'),
    },
    {
        'MATERIAL': 'PVC',
        'DIAMETER_RANGE': (Q(20, 'mm'), Q(30, 'mm')),
        'PRICE_PER_LENGTH': Q(0.3, 'usd/m'),
    }
]