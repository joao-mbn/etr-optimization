import pandas as pd

from global_constants import (ALL_CONDITIONS_EXCEL, COMPLETE_RESULTS_TAB, COST_TAB,
                              DETAILED_COST_TAB, APPROVEDS_ONLY_EXCEL, ROOT_PATH,
                              STANDARDIZED_COST_TAB)
from visualization._cost_relationship_surface import cost_relationship_surface
from visualization._detailed_cost_chart import detailed_cost_chart
from visualization._pareto_chart import pareto_chart, get_regression_comprehensive_coefficients_table
from visualization._predicted_costs_tri_surface import predicted_costs_tri_surface
from visualization._recovery_cost_relationship_chart import recovery_cost_relationship_chart


def generate_charts(save_fig: bool = False):

    cost_df = pd.read_excel(f'{ROOT_PATH}{APPROVEDS_ONLY_EXCEL}', COST_TAB)
    standardized_cost_df = pd.read_excel(f'{ROOT_PATH}{APPROVEDS_ONLY_EXCEL}', STANDARDIZED_COST_TAB)
    detailed_cost_df = pd.read_excel(f'{ROOT_PATH}{APPROVEDS_ONLY_EXCEL}', DETAILED_COST_TAB)
    complete_results_df = pd.read_excel(f'{ROOT_PATH}{APPROVEDS_ONLY_EXCEL}', COMPLETE_RESULTS_TAB)
    all_conditions_complete_results_df = pd.read_excel(f'{ROOT_PATH}{ALL_CONDITIONS_EXCEL}', COMPLETE_RESULTS_TAB)

    pareto_chart(get_regression_comprehensive_coefficients_table(standardized_cost_df), save_fig)
    detailed_cost_chart(detailed_cost_df, save_fig)
    recovery_cost_relationship_chart(complete_results_df, save_fig)
    sliced_charts(cost_df, standardized_cost_df, all_conditions_complete_results_df, save_fig)


def sliced_charts(cost_df, standardized_cost_df, all_conditions_complete_results_df, save_fig):
    for extractant_name in all_conditions_complete_results_df['extractant'].unique().tolist():
        for extractant_concentration in all_conditions_complete_results_df['extractant concentration'].unique().tolist():

            cost_df_slice = cost_df.query(f'extractant == "{extractant_name}" and `extractant concentration` == {extractant_concentration}')
            if len(cost_df_slice) > 0:
                cost_relationship_surface(cost_df_slice, save_fig)

            all_conditions_complete_results_df_slice = all_conditions_complete_results_df.query(f'extractant == "{extractant_name}" and `extractant concentration` == {extractant_concentration}')
            if len(all_conditions_complete_results_df_slice) > 0:
                predicted_costs_tri_surface(all_conditions_complete_results_df_slice, save_fig)

            standardized_cost_df_slice = standardized_cost_df.query(f'extractant == "{extractant_name}" and `extractant concentration` == {extractant_concentration}')
            if len(standardized_cost_df_slice) > 0:
                pareto_chart(get_regression_comprehensive_coefficients_table(standardized_cost_df_slice), save_fig, extractant_name, extractant_concentration)