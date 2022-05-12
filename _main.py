from statistics import mean, median

from cost._costs import calculate_cost
from mass_balance._solve_many import solve_many
from templates._classes import Proton
from templates._models import Project

from visualization._approveds_table import approveds_table


def main(projects: list[Project]):
    """
    - Solves all systems of equations for a given area of investigation, between multiple:
        - Type of Extractant
        - Extractant Concentration
        - pHi
        - A/O Ratio
        - Number of Cells
    - Calculates the cost of each one.
    - Defines the best solution.
    - Provides data visualization.
    """

    for project in projects:

        # Solve systems
        project.pivot_table, project.approved_conditions = solve_many(
            project.cut,
            project.distribution_ratio_model,
            project.rees,
            Proton(),
            project.max_cells_interval,
            project.pHi_interval,
            project.ao_ratio_interval,
            project.required_raffinate_purity,
        )
        # Calculate cost
        for condition in project.approved_conditions:

            condition.cost = calculate_cost(condition, project.extractant, project.solvent)
            project.pivot_table.approveds.highest_cost = max(project.pivot_table.approveds.highest_cost, condition.cost)
            project.pivot_table.approveds.lowest_cost = min(project.pivot_table.approveds.lowest_cost, condition.cost)

            condition.extractant = project.extractant.name
            condition.extractant_concentration = project.extractant.volumetric_concentration

        project.pivot_table.approveds.average_cost = mean(condition.cost for condition in project.approved_conditions)
        project.pivot_table.approveds.cost_median = median(condition.cost for condition in project.approved_conditions)

        # Define best solution
        project.approved_conditions.sort(key=lambda condition: condition.cost)

        # Visualize data
        approveds_table(project.approved_conditions)

        #print(project.approved_conditions[0].__dict__)


