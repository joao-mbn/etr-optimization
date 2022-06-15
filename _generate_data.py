from cost._costs import calculate_cost
from mass_balance._solve_many import solve_many
from templates._classes import Proton
from templates._models import Project, Condition
from visualization._table_manipulation import save_conditions_in_excel


def calculate(projects: list[Project]):
    """
    - Solves all systems of equations for a given area of investigation, between multiple:
        - Type of Extractant
        - Extractant Concentration
        - pHi
        - A/O Ratio
        - Number of Cells
    - Calculates the cost of each one.
    - Saves the data.
    """

    all_projects_approved_conditions: list[Condition] = []

    for project in projects:

        # Solve systems
        project.approved_conditions = solve_many(
            project.cut,
            project.distribution_ratio_model,
            project.rees,
            Proton(),
            project.max_cells_interval,
            project.pHi_interval,
            project.ao_ratio_interval,
            project.required_raffinate_purity,
            project.minimal_recovery,
        )

        # Calculate cost
        for condition in project.approved_conditions:

            condition.costs = calculate_cost(condition, project)
            condition.extractant = project.extractant.name
            condition.extractant_concentration = project.extractant.volumetric_concentration

        all_projects_approved_conditions += project.approved_conditions

    # Save data to an excel spreadsheet
    save_conditions_in_excel(all_projects_approved_conditions)


