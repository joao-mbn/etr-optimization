import pandas as pd

from global_constants import (COST_TAB, DETAILED_COST_TAB, EXCEL_FILE, ROOT_PATH,
                              STANDARDIZED_COST_TAB)
from visualization._cost_relationship_surface import cost_relationship_surface
from visualization._detailed_cost_chart import detailed_cost_chart
from visualization._pareto_chart import pareto_chart


def generate_charts(save_fig: bool = False):

    cost_df = pd.read_excel(f'{ROOT_PATH}{EXCEL_FILE}', COST_TAB)
    standardized_cost_df = pd.read_excel(f'{ROOT_PATH}{EXCEL_FILE}', STANDARDIZED_COST_TAB)
    detailed_cost_df = pd.read_excel(f'{ROOT_PATH}{EXCEL_FILE}', DETAILED_COST_TAB)

    for extractant_name in cost_df['extractant'].unique().tolist():
        for extractant_concentration in cost_df['extractant concentration'].unique().tolist():
            df_slice = cost_df.query(f'extractant == "{extractant_name}" and `extractant concentration` == {extractant_concentration}')

            if len(df_slice) > 0:
                cost_relationship_surface(df_slice, save_fig)

                standardized_cost_df_slice = standardized_cost_df[standardized_cost_df.index.isin(df_slice.index)]
                pareto_chart(standardized_cost_df_slice, save_fig, extractant_name, extractant_concentration)

    detailed_cost_chart(detailed_cost_df, save_fig)
