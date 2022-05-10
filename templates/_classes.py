from templates._types import Vector, Number

# Classes make physical sense, where models do not.

class Element():
    def __init__(self, name, symbol=None, atomic_number=None):
        self.name: str = name
        self.symbol: str = symbol
        self.atomic_number: int = atomic_number


class Substance():

    def __init__(self, price, name) -> None:
        self.price: Number = price
        self.name: str = name


class Equipment():

    def __init__(self, price, name = None) -> None:
        self.price: Number = price
        self.name: str = name


class Proton(Element):
    def __init__(self, feed_concentration=0.5, cells_concentrations = []):

        super().__init__(name='proton', symbol='H', atomic_number=1)

        self.feed_concentration: Number = feed_concentration
        self.cells_concentrations: Vector = cells_concentrations


class Ree(Element):

    def __init__(self,
                 aq_feed_concentration,
                 name,
                 symbol = None,
                 atom_molar_mass = None,
                 oxide_molar_mass = None,
                 atomic_number = None,
                 stoichiometric_proportion = 3,
                 org_feed_concentration = 0,
                 model_coefficients = [],
                 cells_aq_concentrations = [],
                 cells_org_concentrations = [],
                 distribution_ratios = []):

        super().__init__(name=name, symbol=symbol, atomic_number=atomic_number)

        self.aq_feed_concentration: Number = aq_feed_concentration
        self.org_feed_concentration: Number = org_feed_concentration
        self.atom_molar_mass: Number = atom_molar_mass
        self.oxide_molar_mass: Number = oxide_molar_mass
        self.stoichiometric_proportion: Number = stoichiometric_proportion
        self.model_coefficients: Vector = model_coefficients
        self.cells_aq_concentrations: Vector = cells_aq_concentrations
        self.cells_org_concentrations: Vector = cells_org_concentrations
        self.distribution_ratios: Vector = distribution_ratios


class Extractant(Substance):

    volume: Number = 0

    def __init__(self, price, name, volumetric_concentration, molecular_weight, purity, density, volatilization_rate, pKa):
        super().__init__(price, name)

        self.volumetric_concentration: float = volumetric_concentration
        self.purity: float = purity
        self.density: Number = density
        self.volatilization_rate: Number = volatilization_rate
        self.molar_weight: Number = molecular_weight
        self.pKa = pKa
        self.mass_concentration: Number = volumetric_concentration * density * purity
        self.molar_concentration: Number = self.mass_concentration / molecular_weight


class Solvent(Substance):

    volume: Number = 0

    def __init__(self, price, name, volumetric_concentration, molecular_weight, purity, density, volatilization_rate):
        super().__init__(price, name)

        self.volumetric_concentration: float = volumetric_concentration
        self.purity: float = purity
        self.density: Number = density
        self.volatilization_rate: Number = volatilization_rate
        self.molar_weight: Number = molecular_weight
        self.mass_concentration: Number = volumetric_concentration * density * purity
        self.molar_concentration: Number = self.mass_concentration / molecular_weight