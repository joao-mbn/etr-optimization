import pandas as pd

from global_constants import (ALL_CONDITIONS_EXCEL, APPROVEDS_ONLY_EXCEL,
                              COMPLETE_RESULTS_TAB, CONCENTRATED_FEED_EXCEL,
                              COST_TAB, DETAILED_COST_TAB, ROOT_PATH,
                              STANDARDIZED_COST_TAB)
from visualization._cost_relationship_surface import cost_relationship_surface
from visualization._costs_tri_surface import create_multiple_costs_tri_surface
from visualization._detailed_cost_chart import detailed_cost_chart
from visualization._pareto_chart import (
    get_regression_comprehensive_coefficients_table, pareto_chart)
from visualization._recovery_cost_relationship_chart import \
    recovery_cost_relationship_chart


def generate_charts(save_fig: bool = False) -> None:

    detailed_cost_df = pd.read_excel(f'{ROOT_PATH}{CONCENTRATED_FEED_EXCEL}', DETAILED_COST_TAB)
    complete_results_df = pd.read_excel(f'{ROOT_PATH}{APPROVEDS_ONLY_EXCEL}', COMPLETE_RESULTS_TAB)

    all_conditions_cost_df = pd.read_excel(f'{ROOT_PATH}{ALL_CONDITIONS_EXCEL}', COST_TAB)
    all_conditions_standardized_cost_df = pd.read_excel(f'{ROOT_PATH}{ALL_CONDITIONS_EXCEL}', STANDARDIZED_COST_TAB)
    all_conditions_complete_results_df = pd.read_excel(f'{ROOT_PATH}{ALL_CONDITIONS_EXCEL}', COMPLETE_RESULTS_TAB)

    # detailed_cost_chart(detailed_cost_df, save_fig)
    # recovery_cost_relationship_chart(complete_results_df, save_fig)
    pareto_chart(get_regression_comprehensive_coefficients_table(all_conditions_standardized_cost_df), save_fig)
    # create_multiple_costs_tri_surface(all_conditions_complete_results_df, save_fig)

    # sliced_charts(all_conditions_cost_df, all_conditions_standardized_cost_df, all_conditions_complete_results_df, save_fig)


def sliced_charts(cost_df, standardized_cost_df, complete_results_df, save_fig):

    for extractant_name in complete_results_df['extractant'].unique().tolist():
        for extractant_concentration in complete_results_df['extractant concentration'].unique().tolist():

            # cost_df_slice = cost_df.query(f'extractant == "{extractant_name}" and `extractant concentration` == {extractant_concentration}')
            # if len(cost_df_slice) > 0:
            #     cost_relationship_surface(cost_df_slice, save_fig)

            # standardized_cost_df_slice = standardized_cost_df[standardized_cost_df.index.isin(cost_df_slice.index)]
            # if len(standardized_cost_df_slice) > 0:
            #     pareto_chart(get_regression_comprehensive_coefficients_table(standardized_cost_df_slice), save_fig, extractant_name, extractant_concentration)

            complete_results_df_slice = complete_results_df.query(f'extractant == "{extractant_name}" and `extractant concentration` == {extractant_concentration}')
            if len(complete_results_df_slice) > 0:
                create_multiple_costs_tri_surface(complete_results_df_slice, save_fig)
