from templates._units import quantity as Q

HCL = {
    'PRICE': Q(1, 'usd/kg'),
    'DENSITY': Q(1.17, 'kg/L'),
    'MOLAR_MASS': Q(5.453, 'g/mol'),
    'VOLUMETRIC_CONCENTRATION': Q(0.37, 'v/v'),
    'MOLAR_CONCENTRATION': Q(2.21, 'mol/L'),
}

WATER = {
    'DENSITY': Q(997, 'kg/m^3'), # @25ºC, 1atm
}

FEED_LIQUOR = {
    'PRICE': Q(1, 'usd/kg'),
}

ISOPARAFFIN = {
    'NAME': 'Isoparaffin',
    'PRICE': Q(8.9, 'usd/kg'),
    'PURITY': Q(0.99),
    'DENSITY': Q(1, 'kg/L'),
    'VOLATILIZATION_RATE': Q(1, 'kg m^-2 s^-1'),
    'MOLECULAR_WEIGHT': Q(1, 'g/mol'),
}

D2EHPA = {
    'NAME': 'D2EHPA',
    'PRICE': Q(15.52, 'usd/L'),
    'DENSITY': Q(0.97, 'kg/L'),
    'PURITY': Q(0.95),
    'VOLATILIZATION_RATE': Q(1, 'kg m^-2 s^-1'),
    'MOLECULAR_WEIGHT': Q(1, 'g/mol'),
    'PKA': Q(3.32),
}

P507 = {
    'NAME': 'P507',
    'PRICE': Q(80.75, 'usd/L'),
    'DENSITY': Q(0.95, 'kg/L'),
    'PURITY': Q(0.95),
    'VOLATILIZATION_RATE': Q(1, 'kg m^-2 s^-1'),
    'MOLECULAR_WEIGHT': Q(1, 'g/mol'),
    'PKA': Q(4.10),
}

CYANEX_572 = {
    'NAME': 'Cyanex 572',
    'PRICE': Q(208.5, 'usd/L'),
    'DENSITY': Q(0.93, 'kg/L'),
    'PURITY': Q(0.9),
    'VOLATILIZATION_RATE': Q(1, 'kg m^-2 s^-1'),
    'MOLECULAR_WEIGHT': Q(1, 'g/mol'),
    'PKA': Q(6.37),
}

EXTRACTANTS = [D2EHPA, P507, CYANEX_572]
SOLVENTS = [ISOPARAFFIN]