from multiprocessing import dummy
from typing import Any
from numpy import ndarray

import pandas as pd
from helpers._common import create_sub_dataframe
from helpers._utils import standardize
from pint import Quantity
from templates._models import Condition

from visualization._excel import save_to_new_excel


def save_conditions_in_excel(approveds: list[Condition]) -> None:
    """
    Sends the results to an excel file, with data of the approveds.

    - Removes undesired values.
    - Formats the values.
    - Saves a metadata about the dataset (a pivot-table, basically).
    - Saves a standardized values table.
    """

    df = transform_conditions_to_dataframe(approveds)

    cost_df = create_sub_dataframe(df, white_list_substrings = ['total cost', 'extractant', 'cell', 'pHi', 'ao ratio'],
                                   black_list_substrings = ['raw total cost', 'extractant loss'])
    detailed_cost_df = create_sub_dataframe(df, white_list_substrings = ['extractant', 'cell', 'pHi', 'ao ratio', 'loss', 'interest', 'cost'])
    process_df = create_sub_dataframe(df, black_list_substrings = ['cost', 'loss', 'interest'])

    df.sort_values(by=['total cost (usd)'], inplace=True)
    cost_df.sort_values(by=['total cost (usd)'], inplace=True)
    detailed_cost_df.sort_values(by=['raw total cost (usd)'], inplace=True)
    process_df.sort_values(by=['n cells', 'ao ratio', 'pHi'], inplace=True)

    cost_df['ext + concentration'] = cost_df['extractant'].apply(lambda x: f'{x}_') + cost_df['extractant concentration'].apply(lambda x: f'{x * 100:.0f}%').astype(str)
    dummy_df = pd.get_dummies(cost_df['ext + concentration'], drop_first = True)
    cost_df = cost_df.join(dummy_df)
    cost_df.drop('ext + concentration', axis=1, inplace=True)

    cost_pivot_table = cost_df.describe(include='all')
    standardized_cost_df = standardize_dataframe(cost_df, cost_pivot_table).rename(columns={'total cost (usd)': 'total cost'})

    save_to_new_excel([
        {'df': cost_df, 'name': 'Custos'},
        {'df': standardized_cost_df, 'name': 'Custos Padronizados'},
        {'df': cost_pivot_table, 'name': 'Tabela Pivô de Custos', 'index': True},
        {'df': detailed_cost_df, 'name': 'Custos Detalhados'},
        {'df': process_df, 'name': 'Resultados do Processo'},
        {'df': df, 'name': 'Resultados Completos'}
    ])


def transform_conditions_to_dataframe(conditions: list[Condition]) -> pd.DataFrame:
    data = [condition.__dict__ for condition in conditions]
    df = pd.json_normalize(data)
    df.columns = df.columns.str.removeprefix('costs.')
    add_units_to_columns(df)
    df = df.applymap(lambda value: value.magnitude if isinstance(value, Quantity) else value)
    return df


def standardize_dataframe(df: pd.DataFrame, pivot_table: pd.DataFrame) -> pd.DataFrame:
    mean_std_df = pivot_table.loc[['mean', 'std']]
    standardized_df = pd.DataFrame()
    for column in mean_std_df.columns:
        column_mean = mean_std_df.loc['mean', column]
        column_standard_deviation = mean_std_df.loc['std', column]
        standardized_df[column] = df[column].apply(lambda value: standardize(value, column_mean, column_standard_deviation))

    return standardized_df


def add_units_to_columns(df: pd.DataFrame) -> None:
    for column_name, value in zip(df.columns, df.loc[0]):
        unit = '' if not isinstance(value, Quantity) or value.units.dimensionless else f'({value.units})'.replace(' ', '')
        unitted_column_name = f'{column_name} {unit}'.replace('_', ' ').strip()
        df.rename(columns={column_name: unitted_column_name}, inplace=True)
