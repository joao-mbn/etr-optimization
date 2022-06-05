from typing import Callable

from helpers._utils import default_if_none
from numpy import inf
from pint import Quantity
from static_values._substances import MONAZITE

from templates._classes import Extractant, Ree, Solvent
from templates._factories import (extractant_factory, rees_factory,
                                  solvent_factory)
from templates._types import Number, Scalar
from templates._units import quantity as Q

from mass_balance._distribution_ratio_models import logD_x_pH

# Classes make physical sense, where models do not.

class Condition():

    cost: Scalar = Q(inf, 'usd')
    extractant: str = ''
    extractant_concentration: Number = 0

    def __init__(self, n_cells, ao_ratio, pHi, purity, recovery, separation_factor,
                 mass_of_reo_product_at_feed, mass_of_reo_product_at_raffinate,
                 moles_of_ree_product_at_feed, moles_of_ree_product_at_raffinate,
                 pH_at_raffinate):

        self.n_cells: Quantity[int] = Q(n_cells)
        self.ao_ratio: Scalar = Q(ao_ratio)
        self.pHi: Scalar = Q(pHi)
        self.purity: Quantity[float] = Q(purity)
        self.recovery: Quantity[float] = Q(recovery)
        self.separation_factor: Number = separation_factor
        self.mass_of_reo_product_at_feed : Scalar = Q(mass_of_reo_product_at_feed, 'g/L')
        self.mass_of_reo_product_at_raffinate: Scalar = Q(mass_of_reo_product_at_raffinate, 'g/L')
        self.moles_of_ree_product_at_feed: Scalar = Q(moles_of_ree_product_at_feed, 'mol/L')
        self.moles_of_ree_product_at_raffinate: Scalar = Q(moles_of_ree_product_at_raffinate, 'mol/L')
        self.pH_at_raffinate: Scalar = Q(pH_at_raffinate)

class Project():

    approved_conditions = list[Condition]

    def __init__(self, rees, extractant, cut, max_cells_interval, pHi_interval, distribution_ratio_model = logD_x_pH,
                 ao_ratio_interval = (0.5, 2), required_raffinate_purity = 0.995, minimal_recovery = 0.15,
                 solvent = None, mineral = MONAZITE, reos_of_interest_mineral_content = 1):

        self.rees: list[Ree] = rees_factory(rees)
        self.extractant: Extractant = extractant_factory(extractant)
        self.solvent: Solvent = solvent_factory(default_if_none(solvent, dict(name = 'Isoparaffin',
                                                                              concentration = 1 - self.extractant.volumetric_concentration)))
        self.cut: str = cut
        self.distribution_ratio_model: Callable[..., Number] = distribution_ratio_model
        self.max_cells_interval: tuple[int, int] = max_cells_interval
        self.pHi_interval: tuple[Number, Number] = pHi_interval
        self.ao_ratio_interval: tuple[Number, Number] = ao_ratio_interval
        self.required_raffinate_purity: float = required_raffinate_purity
        self.minimal_recovery: float = minimal_recovery
        self.mineral: dict[str, str | Scalar] = mineral
        self.reos_of_interest_mineral_content: float = reos_of_interest_mineral_content
