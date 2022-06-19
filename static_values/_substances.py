from templates._units import quantity as Q

HCL = {
    'PRICE': Q(200, 'usd/ton'), # loosely estimated average from https://www.made-in-china.com/products-search/hot-china-products/Hydrochloric_Acid_Price.html
    'DENSITY': Q(1.17, 'kg/L'),
    'MOLAR_MASS': Q(35.453, 'g/mol'),
    'VOLUMETRIC_CONCENTRATION': Q(0.34, 'v/v'),
    'MOLAR_CONCENTRATION': Q(11.19, 'mol/L'),
}

WATER = {
    'DENSITY': Q(997, 'kg/m^3'), # taken from https://www.sigmaaldrich.com/BR/pt/product/sial/denwat
}

ISOPARAFFIN = {

    # Kerosene average properties used
    # https://en.wikipedia.org/wiki/Kerosene#:~:text=Kerosene%20is%20a%20low%2Dviscosity,10%20and%2016%20carbon%20atoms

    'NAME': 'Isoparaffin',
    'PRICE': Q(1.54, 'usd/L'), # https://www.indiamart.com/proddetail/deodorised-kerosene-oil-22631634230.html?pos=1&pla=n
    'PURITY': Q(0.98),
    'DENSITY': Q(0.78, 'kg/L'),
    'MOLECULAR_WEIGHT': Q(180, 'g/mol'), # https://en.wikipedia.org/wiki/Tridecane
    'SOLUBILITY_IN_WATER': Q(0.007, 'g/L'),
}

D2EHPA = {
    # pKa, MW, density from
    # QI, D.,  Hydrometallurgy of Rare Earths, [S.l.], Elsevier, 2018. p. 187–389. DOI: 10.1016/B978-0-12-813920-2.00002-7.
    'NAME': 'D2EHPA',
    'PRICE': Q(15.52, 'usd/L'),
    'DENSITY': Q(0.97, 'kg/L'),
    'PURITY': Q(0.95),
    'MOLECULAR_WEIGHT': Q(322.43, 'g/mol'),
    'PKA': Q(3.32),
}

P507 = {
    # pKa, MW, density from
    # QI, D.,  Hydrometallurgy of Rare Earths, [S.l.], Elsevier, 2018. p. 187–389. DOI: 10.1016/B978-0-12-813920-2.00002-7.
    'NAME': 'P507',
    'PRICE': Q(80.75, 'usd/L'),
    'DENSITY': Q(0.95, 'kg/L'),
    'PURITY': Q(0.95),
    'MOLECULAR_WEIGHT': Q(306.4, 'g/mol'),
    'PKA': Q(4.10),
}

CYANEX_572 = {

    # PAVÓN, S., KUTUCU, M., COLL, T., et al. "Comparison of Cyanex 272 and Cyanex 572 on the separation of Neodymium from a Nd/Tb/Dy mixture by pertraction",
    # Journal of Chemical Technology and Biotechnology, v. 93, 1 set. 2017. DOI: 10.1002/jctb.5458.

    # pKa hasn't been disclosed, but it has been guessed in the literature that Cyanex 572 might be a mixture of
    # Cyanex 272 (pKa = 6.37; phosphinic acid) and a phosphonic acid (like P507, pKa = 4.10).
    # An average value of 5 has been taken as a first guess.

    'NAME': 'Cyanex 572',
    'PRICE': Q(208.5, 'usd/L'),
    'DENSITY': Q(0.933, 'kg/L'),
    'PURITY': Q(1), # Assumed
    'MOLECULAR_WEIGHT': Q(310, 'g/mol'),
    'PKA': Q(5), # Estimated
}

MONAZITE = {
    # From Araxá's mine
    # OLIVEIRA, A. L. B. de, CARNEIRO, M. C., ALCOVER NETO, A., et al.
    # Digestão de amostras geológicas para a quantificação de elementos das terras raras: Uma abordagem sustentável. [S.l.], CETEM/MCTI, 2020.
    # Disponível em: http://mineralis.cetem.gov.br/handle/cetem/2370.
    'NAME': 'Monazite',
    'PRICE': Q(1900, 'usd/ton'), # taken from "monazite price" search on Google
    'REO_CONTENT': Q(0.55),
    'REOS_DISTRIBUTION': {
        'Sc': Q(0.0036),
        'Y':  Q(0.0124),
        'La': Q(0.2350),
        'Ce': Q(0.4920),
        'Pr': Q(0.0416),
        'Nd': Q(0.1637),
        'Sm': Q(0.0249),
        'Eu': Q(0.0045),
        'Gd': Q(0.0128),
        'Tb': Q(0.0020),
        'Dy': Q(0.0035),
        'Ho': Q(0.0000),
        'Er': Q(0.0015),
        'Tm': Q(0.0013),
        'Yb': Q(0.0006),
        'Lu': Q(0.0005),
    }
}

XENOTIME = {
    # From Pitinga's mine
    # RODRIGUES, R. C. "Lixiviação alcalina do concentrado de xenotima",
    # JORNADA DE INICIAÇÃO CIENTÍFICA. Accepted: 2013-02-01T16:03:07Z, v. 9, 2001.
    # Disponível em: http://mineralis.cetem.gov.br/handle/cetem/891. Acesso em: 29 maio 2022.
    'NAME': 'Xenotime',
    'PRICE': Q(1900, 'usd/ton'), # Assumed equal to that of Monazite
    'REO_CONTENT': Q(0.616),
    'REOS_DISTRIBUTION': {
        'Sc': Q(0.0007),
        'Y':  Q(0.4538),
        'La': Q(0.0072),
        'Ce': Q(0.0268),
        'Pr': Q(0.0065),
        'Nd': Q(0.0166),
        'Sm': Q(0.0124),
        'Eu': Q(0.0000),
        'Gd': Q(0.0217),
        'Tb': Q(0.0186),
        'Dy': Q(0.1071),
        'Ho': Q(0.0287),
        'Er': Q(0.1149),
        'Tm': Q(0.0216),
        'Yb': Q(0.1423),
        'Lu': Q(0.0192),
    }
}

EXTRACTANTS = [D2EHPA, P507, CYANEX_572]
SOLVENTS = [ISOPARAFFIN]