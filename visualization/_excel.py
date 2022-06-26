import pandas as pd
from openpyxl import load_workbook
from global_constants import ROOT_PATH, APPROVEDS_ONLY_EXCEL
from helpers._utils import value_or_default

def save_to_existing_excel(sheets: list[dict[str, pd.DataFrame| str | bool]], path: str = ROOT_PATH, file: str = APPROVEDS_ONLY_EXCEL) -> None:
    book = load_workbook(f'{path}{file}')
    writer = get_writer(path, file)
    writer.book = book
    writer.sheets = dict((ws.title, ws) for ws in writer.book.worksheets)

    add_sheets(sheets, writer)
    persist(writer)


def save_to_new_excel(sheets: list[dict[str, pd.DataFrame| str | bool]], path: str = ROOT_PATH, file: str = APPROVEDS_ONLY_EXCEL) -> None:
    writer = get_writer(path, file)

    add_sheets(sheets, writer)
    persist(writer)


def get_writer(path: str = ROOT_PATH, file: str = APPROVEDS_ONLY_EXCEL) -> pd.ExcelWriter:
    return pd.ExcelWriter(f'{path}{file}', engine='openpyxl')


def add_sheets(sheets: list[dict[str, pd.DataFrame| str | bool]], writer: pd.ExcelWriter) -> None:
    for sheet in sheets:
        df: pd.DataFrame = sheet['df']
        df.to_excel(writer, sheet['name'], index = value_or_default(sheet, 'index', False))


def persist(writer: pd.ExcelWriter) -> None:
    writer.save()
    writer.close()