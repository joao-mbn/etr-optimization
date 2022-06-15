import matplotlib.pyplot as plt
import pandas as pd
from global_constants import CHARTS_RESULTS_FOLDER_PATH
from matplotlib.ticker import PercentFormatter

from visualization._regression import get_regression_coefficients_table


def pareto_chart(df_slice: pd.DataFrame, save_fig: bool = False,
                 extractant_name: str = '', extractant_concentration: int = 0) -> None:

    coefficients_df = get_regression_coefficients_table(df_slice)
    coefficients_df['absolute value (%)'] = (coefficients_df['value'].abs() * 100
                                             / coefficients_df['value'].abs().sum()).round(2)
    coefficients_df['accumulated absolute value (%)'] = (coefficients_df['absolute value (%)'].cumsum() * 100
                                                         / coefficients_df['absolute value (%)'].sum()).round(2)
    coefficients_df.drop(coefficients_df[coefficients_df['absolute value (%)'] == 0].index, inplace=True)

    fig, ax = plt.subplots(figsize=(16, 10))

    bars = ax.bar(coefficients_df['name'], coefficients_df['absolute value (%)'], color = '#0066ff')
    ax.set_title('Importância das Variáveis no Custo Total de Produção')
    ax.yaxis.set_major_formatter(PercentFormatter())
    ax.set_xlabel('Efeitos Padronizados')
    ax.set_ylabel('Importância Absoluta (%)')
    ax.bar_label(bars)

    ax2 = ax.twinx()
    ax2.plot(coefficients_df['name'], coefficients_df['accumulated absolute value (%)'], color='red', marker='D', ms=7)
    ax2.axhline(80, color='orange', linestyle='dashed')
    ax2.yaxis.set_major_formatter(PercentFormatter())
    ax2.set_ylabel('Importância Absoluta Acumulada (%)')

    fig.autofmt_xdate(rotation=60)
    plt.show() if not save_fig else plt.savefig(f'{CHARTS_RESULTS_FOLDER_PATH}Pareto {extractant_name} {round(extractant_concentration * 100)}%.png',
                                                bbox_inches='tight')
