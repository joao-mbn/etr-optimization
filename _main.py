from statistics import mean, median

from cost._costs import calculate_cost
from helpers._utils import value_or_default
from mass_balance._solve_many import solve_many
from templates._classes import Proton
from templates._models import Project
from templates._factories import rees_factory, extractant_factory, solvent_factory


def main(projects: list[Project]):

    for project in projects:

        project.pivot_table, project.approved_conditions = solve_many(  # type: ignore
            project.cut,
            project.distribution_ratio_model,
            project.rees,
            Proton(),
            project.max_cells_interval,
            project.pHi_interval,
            project.ao_ratio_interval,
            project.required_raffinate_purity,
        )

        for condition in project.approved_conditions:

            condition.cost = calculate_cost(condition, project.extractant, project.solvent)
            project.pivot_table.approveds.highest_cost = max(project.pivot_table.approveds.highest_cost, condition.cost)
            project.pivot_table.approveds.lowest_cost = min(project.pivot_table.approveds.lowest_cost, condition.cost)

        project.pivot_table.approveds.average_cost = mean(condition.cost for condition in project.approved_conditions)
        project.pivot_table.approveds.cost_median = median(condition.cost for condition in project.approved_conditions)
