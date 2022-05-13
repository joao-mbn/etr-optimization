from pandas import ExcelWriter
from templates._models import Condition
from helpers._common import transform_conditions_to_dataframe

def approveds_table(approveds: list[Condition]) -> None:
    """
    Sends the results to an excel file, with data of the approveds
    and metadata about the dataset (a pivot-table, basically).
    """

    # Create dataframe out of the approveds
    df = transform_conditions_to_dataframe(approveds)

    # Creates the table with the data and the pivot table with the metadata
    highlights = df.describe(include='all')

    # Saves it to an excel file
    writer = ExcelWriter('C:/Users/joao.batista/Desktop/aprovados.xlsx', engine='openpyxl')
    df.to_excel(writer, 'Condições Aprovadas')
    highlights.to_excel(writer, 'Highlights')
    writer.save()
    writer.close()