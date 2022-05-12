from typing import Callable

from pint import Quantity

from helpers._utils import default_if_none
from numpy import inf

from templates._classes import Extractant, Ree, Solvent
from templates._factories import (extractant_factory, rees_factory,
                                  solvent_factory)
from templates._types import Number, Scalar
from templates._units import quantity as Q

# Classes make physical sense, where models do not.

class Condition():

    cost: Scalar = Q(inf, 'usd')

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


class Approveds():

    average_separation_factor: Number = 0
    average_recovery: Number = 0
    average_cost: Scalar = Q(0.0, 'usd')

    separation_factor_median: Number = 0
    recovery_median: float = 0
    cost_median: Scalar = Q(0.0, 'usd')

    highest_average_separation_factor: Number = -inf
    lowest_average_separation_factor: Number = inf
    highest_recovery: float = -inf
    lowest_recovery: float = inf
    highest_purity: float = -inf
    lowest_cost: Scalar = Q(inf, 'usd')
    highest_cost: Scalar = Q(-inf, 'usd')


class PivotTable():

    number_of_tests: int = 0
    total_of_approveds: int = 0
    approveds = Approveds()


class Project():

    pivot_table = PivotTable()
    approved_conditions = list[Condition]

    def __init__(self, rees, extractant, cut, distribution_ratio_model, max_cells_interval, pHi_interval,
                 ao_ratio_interval = (0.5, 2), required_raffinate_purity = 0.995, solvent = None):

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
