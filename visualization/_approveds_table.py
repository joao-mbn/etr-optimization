from typing import Any
import pandas as pd
from pint import Quantity

from templates._models import Condition

def approveds_table(approveds: list[Condition]) -> None:
    """
    Passes the dimensions of the approveds from individual
    results to the columns and send it to excel.
    """
    data = [approved.__dict__ for approved in approveds]
    unitted_columns_names = add_units_to_columns(data[0])
    remove_units_from_data(data)
    df = pd.DataFrame(data)
    df.rename(columns=unitted_columns_names, inplace=True)
    df.to_excel('C:/Users/joao.batista/Desktop/aprovados.xlsx', 'Condições Aprovadas')


def add_units_to_columns(data: dict[str, Any]) -> dict[str, str]:

    columns_to_update = dict()
    for key, value in data.items():
        if isinstance(value, Quantity):
            unit = f'({value.units})'.replace(' ', '') if not value.units.dimensionless else ''
        else:
            unit = ''

        columns_to_update[key] = f'{key} {unit}'.replace('_', ' ')

    return columns_to_update

def remove_units_from_data(data: list[dict[str, Any]]) -> None:
    for row in data:
        for key, value in row.items():
            if isinstance(value, Quantity):
                row[key] = value.magnitude