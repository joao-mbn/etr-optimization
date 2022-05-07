from main import *
from operacao import Operacao
from substancia import Substancia

hcl = Substancia('HCl', 1, {'densidade': 1179, 'concentracao_mm': 0.37, 'MM': 36.5}) #preço em R$/kg
dehpa = Substancia('D2EHPA', 15.52, {'densidade': 0.97, 'pureza': 0.95, 'taxa_perda' : 0.1}) #preço em R$/L
p507 = Substancia('P507', 80.75, {'densidade': 0.95, 'pureza': 0.95, 'taxa_perda' : 0.1}) #preço em R$/L
cyanex272 = Substancia('Cyanex 272', 208.5, {'densidade': 0.93, 'pureza': 0.9, 'taxa_perda' : 0.1}) #preço em R$/L
isoparafina = Substancia('Isoparafina', 8.9, {'pureza': 1, 'taxa_perda' : 0.1}) #preço em R$/L
mixset = Celula('Mixer-Settler', 54200, None, 10) #preco em R$/unit.

# Isotermas de lavagem parecem passíveis de otimização por chutes mais precisos
disprosio = ETR('Disprósio', 'Dy', 600, 99.5, 3.19, 0, 372.998, 2, 3.22552, -0.99999)
holmio = ETR('Hólmio', 'Ho', 40, 99.9, 6.71, 0, 377.858, 2, 3.05008, -0.68760)
H = Proton('Próton', 'H+', None, 0.55)
isoterma = Isoterma(40, 0.6, [H, disprosio, holmio])
operacao = Operacao([disprosio, holmio], p507, 0.26, isoparafina, hcl, mixset, 30, 30, 1, 1, 0.3, 0.3)


# D2EHPA 10%
praseodimio1 = ETR('Praseodímio', 'Pr', 75, 99.5, 0.480, 0, 1021.44, 6, 2.84, -3.6807)
neodimio1 = ETR('Neodímio', 'Nd', 75, 99.5, 12.808, 0, 336.48, 2, 1.0539, -1.7022)
samario1 = ETR('Samário', 'Sm', 10, 99.9, 0.923, 0, 348.72, 2, 1.5262, -1.1515)
operacao1 = Operacao([praseodimio1, neodimio1, samario1], dehpa, 0.1, isoparafina, hcl, mixset, 2, 10, 0.5, 2, 1, 2)
H2 = Proton('Próton', 'H+', None, 10**-2)
isoterma = Isoterma(2, 0.8, [H2, praseodimio1, neodimio1, samario1])

# D2EHPA 6%
praseodimio2 = ETR('Praseodímio', 'Pr', 75, 99.5, 0.480, 0, 1021.44, 6, 0.4026, -1.5661)
neodimio2 = ETR('Neodímio', 'Nd', 75, 99.5, 12.808, 0, 336.48, 2, 0.8569, -1.9035)
samario2 = ETR('Samário', 'Sm', 10, 99.9, 0.923, 0, 348.72, 2, 1.1924, -1.2654)
operacao2 = Operacao([praseodimio2, neodimio2, samario2], dehpa, 0.06, isoparafina, hcl, mixset, 2, 10, 0.5, 2, 1, 2)
H2 = Proton('Próton', 'H+', None, 10**-2)
isoterma = Isoterma(2, 0.8, [H2, praseodimio2, neodimio2, samario2])

# P507 10%
praseodimio3 = ETR('Praseodímio', 'Pr', 75, 99.5, 0.480, 0, 1021.44, 6, 0.7487, -2.3629)
neodimio3 = ETR('Neodímio', 'Nd', 75, 99.5, 12.808, 0, 336.48, 2, 1.6106, -3.3279)
samario3 = ETR('Samário', 'Sm', 10, 99.9, 0.923, 0, 348.72, 2, 2.213, -2.9758)
operacao3 = Operacao([praseodimio3, neodimio3, samario3], p507, 0.1, isoparafina, hcl, mixset, 2, 10, 0.5, 2.5, 1.2, 2)

# P507 6%
praseodimio4 = ETR('Praseodímio', 'Pr', 75, 99.5, 0.480, 0, 1021.44, 6, 6.5856, -11.441)
neodimio4 = ETR('Neodímio', 'Nd', 75, 99.5, 12.808, 0, 336.48, 2, 1.5074, -3.5508)
samario4 = ETR('Samário', 'Sm', 10, 99.9, 0.923, 0, 348.72, 2, 2.1979, -3.4924)
operacao4 = Operacao([praseodimio4, neodimio4, samario4], p507, 0.06, isoparafina, hcl, mixset, 2, 10, 0.5, 2.5, 1.2, 2)

# Cyanex 572 10%
praseodimio5 = ETR('Praseodímio', 'Pr', 75, 99.5, 0.480, 0, 1021.44, 6, 0.393, -2.2876)
neodimio5 = ETR('Neodímio', 'Nd', 75, 99.5, 12.808, 0, 336.48, 2, 1.5592, -3.976)
samario5 = ETR('Samário', 'Sm', 10, 99.9, 0.923, 0, 348.72, 2, 1.9341, -3.2532)
operacao5 = Operacao([praseodimio5, neodimio5, samario5], cyanex272, 0.1, isoparafina, hcl, mixset, 2, 10, 0.5, 2.5, 1.5, 2.5)