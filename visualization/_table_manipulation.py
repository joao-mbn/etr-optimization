from typing import Any

import pandas as pd
from helpers._utils import standardize
from pint import Quantity
from templates._models import Condition


def save_conditions_in_excel(approveds: list[Condition]) -> None:
    """
    Sends the results to an excel file, with data of the approveds.

    - Removes undesired values.
    - Formats the values.
    - Saves a metadata about the dataset (a pivot-table, basically).
    - Saves a standardized values table.
    """

    df = transform_conditions_to_dataframe(approveds)

    cost_df = create_sub_dataframe(df, substrings_columns_should_not_have = ['feed', 'raffinate', 'purity', 'recovery', 'separation factor'])
    process_df = create_sub_dataframe(df, substrings_columns_should_not_have = ['cost', 'extractant', 'ree'])

    sort_df(df, by = ['cost (usd)'])
    sort_df(cost_df, by = ['cost (usd)'])
    sort_df(process_df, by = ['n cells', 'ao ratio', 'pHi'])

    cost_pivot_table = cost_df.describe(include='all')

    standardized_cost_df = standardize_dataframe(cost_df, cost_pivot_table).rename(columns={'cost (usd)': 'cost'})

    writer = pd.ExcelWriter('C:/Users/joao.batista/Desktop/My Repos/etr-optimization/aprovados.xlsx', engine='openpyxl')

    cost_df.to_excel(writer, 'Custos', index = False)
    standardized_cost_df.to_excel(writer, 'Custos Padronizados', index = False)
    cost_pivot_table.to_excel(writer, 'Tabela Pivô de Custos', index = False)
    process_df.to_excel(writer, 'Resultados do Processo', index = False)
    df.to_excel(writer, 'Resultados Completos', index = False)

    writer.save()
    writer.close()

def transform_conditions_to_dataframe(conditions: list[Condition]) -> pd.DataFrame:
    """
    Turns a list of conditions into a dictionary of its properties and than into a dataframe.
    Removes the units from individual cells and set it to the column.
    """
    data = [condition.__dict__ for condition in conditions]
    unitted_columns_names = add_units_to_columns(data[0])
    remove_units_from_data(data)
    df = pd.DataFrame(data)
    df.rename(columns=unitted_columns_names, inplace=True)
    return df

def create_sub_dataframe(df: pd.DataFrame, substrings_columns_should_not_have) -> pd.DataFrame:
    columns_to_remain = [column for column in df.columns if is_column_of_interest(column, substrings_columns_should_not_have)]
    return df[columns_to_remain]

def sort_df(df: pd.DataFrame, by: list[str]) -> None:
    df.sort_values(by=by, inplace=True)

def standardize_dataframe(df: pd.DataFrame, pivot_table: pd.DataFrame) -> pd.DataFrame:
    mean_std_df = pivot_table.loc[['mean', 'std']]
    standardized_df = pd.DataFrame()
    for column in mean_std_df.columns:
        column_mean = mean_std_df.loc['mean', column]
        column_standard_deviation = mean_std_df.loc['std', column]
        standardized_df[column] = df[column].apply(lambda value: standardize(value, column_mean, column_standard_deviation))

    return standardized_df

def add_units_to_columns(data: dict[str, Any]) -> dict[str, str]:
    columns_to_update = dict()
    for key, value in data.items():
        unit = '' if not isinstance(value, Quantity) or value.units.dimensionless else f'({value.units})'.replace(' ', '')
        columns_to_update[key] = f'{key} {unit}'.replace('_', ' ').strip()

    return columns_to_update

def remove_units_from_data(data: list[dict[str, Any]]) -> None:
    for row in data:
        for key, value in row.items():
            if isinstance(value, Quantity):
                row[key] = value.magnitude

def is_column_of_interest(column: str, substrings_columns_should_not_have: list[str]) -> bool:
    return all(substring not in column for substring in substrings_columns_should_not_have)
