from typing import Callable
from templates._types import Number
from numpy import inf
from templates._factories import rees_factory, extractant_factory, solvent_factory
from helpers._utils import default_if_none
from templates._classes import Ree, Extractant, Solvent

# Classes make physical sense, where models do not.

class Condition():

    cost = inf

    def __init__(self, n_cells, ao_ratio, pHi, purity, recovery, separation_factor, product_at_feed, product_at_raffinate, pH_at_raffinate):
        self.n_cells: int = n_cells
        self.ao_ratio: Number = ao_ratio
        self.pHi: Number = pHi
        self.purity: float = purity
        self.recovery: float = recovery
        self.separation_factor: Number = separation_factor
        self.product_at_feed: Number = product_at_feed
        self.product_at_raffinate: Number = product_at_raffinate
        self.pH_at_raffinate = pH_at_raffinate


class Approveds():

    average_separation_factor: Number = 0
    average_recovery: Number = 0
    average_cost: Number = 0

    separation_factor_median: Number = 0
    recovery_median: float = 0
    cost_median: Number = 0

    highest_average_separation_factor: Number = -inf
    lowest_average_separation_factor: Number = inf
    highest_recovery: float = -inf
    lowest_recovery: float = inf
    highest_purity: float = -inf
    lowest_cost: Number = inf
    highest_cost: Number = -inf


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
        self.solvent: Solvent = solvent_factory(
            default_if_none(solvent,
                            dict(name = 'Isoparaffin', concentration = 1 - extractant.volumetric_concentration)))
        self.cut: str = cut
        self.distribution_ratio_model: Callable[..., Number] = distribution_ratio_model
        self.max_cells_interval: tuple[int, int] = max_cells_interval
        self.pHi_interval: tuple[Number, Number] = pHi_interval
        self.ao_ratio_interval: tuple[Number, Number] = ao_ratio_interval
        self.required_raffinate_purity: float = required_raffinate_purity
