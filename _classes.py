from _types import Vector, Number

class Element():
    def __init__(self, name, symbol=None, atomic_number=None):
        self.name: str = name
        self.symbol: str = symbol
        self.atomic_number: int = atomic_number


class Proton(Element):
    def __init__(self, feed_concentration, cells_concentrations = []):
        super().__init__(name='proton', symbol='H', atomic_number=1)
        self.feed_concentration: Number = feed_concentration
        self.cells_concentrations: Vector = cells_concentrations


class Ree(Element):

    def __init__(self, aq_feed_concentration, name, oxide_molar_mass, symbol = None, atomic_number = None, stoichiometric_proportion = 3,
        org_feed_concentration = 0, model_coefficients = [], cells_aq_concentrations = [], cells_org_concentrations = [],
        distribution_ratios = []):

        super().__init__(name=name, symbol=symbol, atomic_number=atomic_number)
        self.aq_feed_concentration: Number = aq_feed_concentration
        self.org_feed_concentration: Number = org_feed_concentration
        self.oxide_molar_mass: Number = oxide_molar_mass
        self.stoichiometric_proportion: Number = stoichiometric_proportion
        self.model_coefficients: Vector = model_coefficients
        self.cells_aq_concentrations: Vector = cells_aq_concentrations
        self.cells_org_concentrations: Vector = cells_org_concentrations
        self.distribution_ratios: Vector = distribution_ratios