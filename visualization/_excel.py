import pandas as pd
from openpyxl import load_workbook
from constants import PATH, EXCEL_FILE

def save_to_existing_excel(dfs: list[pd.DataFrame], sheet_names: list[str]) -> None:

    book = load_workbook(f'{PATH}{EXCEL_FILE}')
    writer = pd.ExcelWriter(f'{PATH}{EXCEL_FILE}', engine='openpyxl')
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)

    for df, sheet_name in zip(dfs, sheet_names):
        df.to_excel(writer, sheet_name, index = False)

    writer.save()
    writer.close()