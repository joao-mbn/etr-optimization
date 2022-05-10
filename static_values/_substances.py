HCL = {
    'PRICE': 1,
    'DENSITY': 1.17,
    'MOLAR_MASS': 35.453,
    'VOLUMETRIC_CONCENTRATION': 0.37, # v/v
    'MOLAR_CONCENTRATION': 12.21 # mol/L
}

WATER = {
    'DENSITY': 997, # kg/m³ @25ºC, 1 atm
}

FEED_LIQUOR = {
    'PRICE': 1,
}

ISOPARAFFIN = {
    'NAME': 'Isoparaffin',
    'PRICE': 8.9, # R$/kg
    'DENSITY': 1,
    'VOLATILIZATION_RATE': 1,
    'MOLECULAR_WEIGHT': 1,
}

D2EHPA = {
    'NAME': 'D2EHPA',
    'PRICE': 15.52, # R$/L
    'DENSITY': 0.97, # kg/L
    'PURITY': 0.95,
    'VOLATILIZATION_RATE': 1,
    'MOLECULAR_WEIGHT': 1,
    'PKA': 3.32,
}

P507 = {
    'NAME': 'P507',
    'PRICE': 80.75, # R$/L
    'DENSITY': 0.95, # kg/L
    'PURITY': 0.95,
    'VOLATILIZATION_RATE': 1,
    'MOLECULAR_WEIGHT': 1,
    'PKA': 4.10,
}

CYANEX_272 = {
    'NAME': 'Cyanex 272',
    'PRICE': 208.5, # R$/L
    'DENSITY': 0.93, # kg/L
    'PURITY': 0.9,
    'VOLATILIZATION_RATE': 1,
    'MOLECULAR_WEIGHT': 1,
    'PKA': 6.37,
}

EXTRACTANTS = [D2EHPA, P507, CYANEX_272]
SOLVENTS = [ISOPARAFFIN]