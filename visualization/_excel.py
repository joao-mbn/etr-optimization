import pandas as pd
from openpyxl import load_workbook
from constants import PATH, EXCEL_FILE
from helpers._utils import value_or_default

def save_to_existing_excel(sheets: list[dict[str, pd.DataFrame| str | bool]]) -> None:

    book = load_workbook(f'{PATH}{EXCEL_FILE}')
    writer = pd.ExcelWriter(f'{PATH}{EXCEL_FILE}', engine='openpyxl')
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)

    add_sheets(sheets, writer)
    persist(writer)


def save_to_new_excel(sheets: list[dict[str, pd.DataFrame| str | bool]]) -> None:

    writer = pd.ExcelWriter(f'{PATH}{EXCEL_FILE}', engine='openpyxl')

    add_sheets(sheets, writer)
    persist(writer)


def add_sheets(sheets: list[dict[str, pd.DataFrame| str | bool]], writer: pd.ExcelWriter) -> None:
    for sheet in sheets:
        df: pd.DataFrame = sheet['df']
        df.to_excel(writer, sheet['name'], index = value_or_default(sheet, 'index', False))


def persist(writer: pd.ExcelWriter) -> None:
    writer.save()
    writer.close()