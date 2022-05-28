from templates._units import quantity as Q

HCL = {
    'PRICE': Q(200, 'usd/ton'),
    'DENSITY': Q(1.17, 'kg/L'),
    'MOLAR_MASS': Q(35.453, 'g/mol'),
    'VOLUMETRIC_CONCENTRATION': Q(0.34, 'v/v'),
    'MOLAR_CONCENTRATION': Q(11.19, 'mol/L'),
}

WATER = {
    'DENSITY': Q(997, 'kg/m^3'),
}

# Kerosene average properties used
ISOPARAFFIN = {
    'NAME': 'Isoparaffin',
    'PRICE': Q(1.54, 'usd/L'),
    'PURITY': Q(0.98),
    'DENSITY': Q(0.78, 'kg/L'),
    'MOLECULAR_WEIGHT': Q(180, 'g/mol'),
    'SOLUBILITY_IN_WATER': Q(0.007, 'g/L'),
}

D2EHPA = {
    'NAME': 'D2EHPA',
    'PRICE': Q(15.52, 'usd/L'),
    'DENSITY': Q(0.97, 'kg/L'),
    'PURITY': Q(0.95),
    'MOLECULAR_WEIGHT': Q(322.43, 'g/mol'),
    'PKA': Q(3.32),
}

P507 = {
    'NAME': 'P507',
    'PRICE': Q(80.75, 'usd/L'),
    'DENSITY': Q(0.95, 'kg/L'),
    'PURITY': Q(0.95),
    'MOLECULAR_WEIGHT': Q(306.4, 'g/mol'),
    'PKA': Q(4.10),
}

CYANEX_572 = {
    # pKa hasn't been disclosed, but it has been guessed in the literature that Cyanex 572 might be a mixture of
    # cyanex 272 (pKa = 6.37; phosphinic acid) and a phosphonic acid (like P507, pKa = 4.10).
    # An average value of 5 has been taken as a first guess.

    'NAME': 'Cyanex 572',
    'PRICE': Q(208.5, 'usd/L'),
    'DENSITY': Q(0.933, 'kg/L'),
    'PURITY': Q(1),
    'VOLATILIZATION_RATE': Q(1, 'kg m^-2 s^-1'), # TODO
    'MOLECULAR_WEIGHT': Q(310, 'g/mol'),
    'PKA': Q(5),
}

MONAZITE = {
    'NAME': 'Monazite',
    'PRICE': Q(1900, 'usd/ton'),
    'REO_CONTENT': Q(0.55),
}

XENOTIME = {
    'NAME': 'Xenotime',
    'PRICE': Q(1900, 'usd/ton'), # Not really known
    'REO_CONTENT': Q(0.616),
}

EXTRACTANTS = [D2EHPA, P507, CYANEX_572]
SOLVENTS = [ISOPARAFFIN]