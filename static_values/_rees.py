SEPARATION_ORDER = ['La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Y', 'Er', 'Tm', 'Yb', 'Lu']

REE_VALENCY = 3
REE_OXIDE_STOICHIOMETRIC_PROPORTION = 2
REE_EXTRACTANT_STOICHIOMETRIC_PROPORTION = 6

PRASEODYMIUM = {
    'NAME': 'Praseodímio',
    'SYMBOL': 'Pr',
    'ATOMIC_WEIGHT': 140.90765, # g/mol, taken from Wikipedia EN
    'OXIDE_WEIGHT': 1021.44, # g/mol, taken from Wikipedia EN
    'VALENCY': REE_VALENCY,
    'OXIDE_STOICHIOMETRIC_PROPORTION': 6
}

NEODYMIUM = {
    'NAME': 'Neodímio',
    'SYMBOL': 'Nd',
    'ATOMIC_WEIGHT': 144.242, # g/mol, taken from Wikipedia EN
    'OXIDE_WEIGHT': 336.48, # g/mol, taken from Wikipedia EN
    'VALENCY': REE_VALENCY,
    'OXIDE_STOICHIOMETRIC_PROPORTION': REE_OXIDE_STOICHIOMETRIC_PROPORTION
}

SAMARIUM = {
    'NAME': 'Samário',
    'SYMBOL': 'Sm',
    'ATOMIC_WEIGHT': 150.36, # g/mol, taken from Wikipedia EN
    'OXIDE_WEIGHT': 348.72, # g/mol, taken from Wikipedia EN
    'VALENCY': REE_VALENCY,
    'OXIDE_STOICHIOMETRIC_PROPORTION': REE_OXIDE_STOICHIOMETRIC_PROPORTION
}

DYSPROSIUM = {
    'NAME': 'Disprósio',
    'SYMBOL': 'Dy',
    'ATOMIC_WEIGHT': 162.5, # g/mol, taken from Wikipedia EN
    'OXIDE_WEIGHT': 372.998, # g/mol, taken from Wikipedia EN
    'VALENCY': REE_VALENCY,
    'OXIDE_STOICHIOMETRIC_PROPORTION': REE_OXIDE_STOICHIOMETRIC_PROPORTION
}

HOLMIUM = {
    'NAME': 'Hólmio',
    'SYMBOL': 'Ho',
    'ATOMIC_WEIGHT': 164.93032, # g/mol, taken from Wikipedia EN
    'OXIDE_WEIGHT': 377.858, # g/mol, taken from Wikipedia EN
    'VALENCY': REE_VALENCY,
    'OXIDE_STOICHIOMETRIC_PROPORTION': REE_OXIDE_STOICHIOMETRIC_PROPORTION
}

REES = [PRASEODYMIUM, NEODYMIUM, SAMARIUM, DYSPROSIUM, HOLMIUM]