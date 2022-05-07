from statistics import mean, median

from cost._costs import calculate_cost
from helpers._utils import value_or_default
from mass_balance._solve_many import solve_many
from templates._classes import Proton
from templates._ree_factory import ree_factory


def main(projects: list[dict]):

    for project in projects:
        project['rees'] = ree_factory(project['rees'])
        project['data_to_pivot_table'], project['conditions_with_pure_enough_raffinate'] = solve_many(
            project['cut'],
            project['distribution_ratio_model'],
            project['rees'],
            Proton(),
            project['max_cells_interval'],
            project['pH_interval'],
            value_or_default(project, 'ao_ratio_interval', (0.5, 2)),
            value_or_default(project, 'required_raffinate_purity', 0.995),
        )

        for condition in project['conditions_with_pure_enough_raffinate']:

            condition['cost'] = calculate_cost(condition, project['extractant'])
            project['data_to_pivot_table']['highest_cost'] = max(project['data_to_pivot_table']['highest_cost'], condition['cost'])
            project['data_to_pivot_table']['lowest_cost'] = min(project['data_to_pivot_table']['lowest_cost'], condition['cost'])

        project['data_to_pivot_table']['average_cost'] = mean(condition['cost'] for condition in project['conditions_with_pure_enough_raffinate'])
        project['data_to_pivot_table']['cost_median'] = median(condition['cost'] for condition in project['conditions_with_pure_enough_raffinate'])
